import logging
import awsutils
import bcutils


def do_terminate(args):
    """
    1. terminate all EC2 instances
    2. terminate all security groups
    """
    nodes_info = bcutils.get_all_nodes_info()
    for region_name in nodes_info:
        sgs_to_delete = set()
        logging.info('Terminating region: {} ...'.format(region_name))
        inst_id_list = [x['id'] for x in nodes_info[region_name]]
        instances = awsutils.get_instances_info(region_name, inst_id_list)
        for item in instances:
            item.terminate()
            logging.info('- terminated {}'.format(item.id))

        logging.info('Deleting security groups for {} ...'.format(region_name))
        sg_id_list = [bcutils.get_security_group_name(region_name)]
        awsutils.delete_security_groups(region_name, sg_id_list)
        logging.info('Deleted {}'.format(sg_id_list))
