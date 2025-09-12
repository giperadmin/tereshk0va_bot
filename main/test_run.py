from main.utils.periodic_tasks import task_sync_from_S3_to_local
from main.utils import s3_data_sync

s3_data_sync.all_s3_to_local()
