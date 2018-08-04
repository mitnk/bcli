read -p "Are you sure to upload local ssh public key to all regions? " -n 1 -r
echo    # move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
fi

keypair=mpb-home-13  # or some name that is meaningful to you
publickeyfile=$HOME/.ssh/id_rsa.pub
regions=$(aws ec2 describe-regions --output text --query 'Regions[*].RegionName')

for region in $regions; do
  echo "uploading to $region ..."
  aws ec2 import-key-pair \
    --region "$region" \
    --key-name "$keypair" \
    --public-key-material "file://$publickeyfile"
done

echo "done."
