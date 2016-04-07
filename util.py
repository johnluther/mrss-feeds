import boto
import mimetypes

cdnUrl = '//s3.amazonaws.com/%s/%s'

profile_name = 'qa_jwplayer'
bucketName    = 'qa.jwplayer.com'

profile_name = 'personal'
bucketName    = 'jwfeeds'

def upload2s3(fp, s3Key):    
    s3_connection = boto.connect_s3(profile_name=profile_name)
    bucket        = s3_connection.get_bucket(bucketName)
    key           = boto.s3.key.Key(bucket, s3Key)
    key.set_contents_from_file(fp, policy='public-read', headers={'Content-Type': mimetypes.guess_type(s3Key)[0]})
    return cdnUrl % (bucketName, s3Key)


def string2s3(string, s3Key):
    s3_connection = boto.connect_s3(profile_name=profile_name)
    bucket        = s3_connection.get_bucket(bucketName)
    key           = boto.s3.key.Key(bucket, s3Key)
    key.set_contents_from_string(string, policy='public-read', headers={'Content-Type': 'application/rss+xml'})
    return cdnUrl % (bucketName, s3Key)