import logging

import awsutils
import constants
import bcutils


def do_terminate(args):
    """
    1. terminate all EC2 instances
    2. terminate all security groups
    """
    nodes_info = bcutils.get_all_nodes_info()
    for region_name in nodes_info:
        sgs_to_delete = set()
        sgs_others = set()
        logging.info('Terminating resources in {} ...'.format(region_name))
        inst_id_list = [x['id'] for x in nodes_info[region_name]]
        instances = awsutils.get_instances_info(region_name, inst_id_list)
        for item in instances:
            if item.state['Name'] == 'terminated':
                logging.info('- instance {} already terminated'.format(item.id))
                continue

            for sg in item.security_groups:
                if sg['GroupName'].startswith(constants.SG_PREFIX):
                    sgs_to_delete.add(sg['GroupId'])
                else:
                    sgs_others.add(sg['GroupId'])

            # remove existing SGs to prevent DependencyViolation when deleting
            item.modify_attribute(Groups=list(sgs_others))
            item.terminate()
            logging.info('- terminated {}'.format(item.id))

        sgs_to_delete = list(sgs_to_delete)
        awsutils.delete_security_groups(region_name, sgs_to_delete)
        logging.info('- deleted security groups: {}'.format(sgs_to_delete))
