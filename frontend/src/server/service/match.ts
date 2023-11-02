import { type CompleteUploadRequest } from "@/utils/z.schema";
import {
  CompleteMultipartUploadCommand,
  CreateMultipartUploadCommand,
  S3Client,
} from "@aws-sdk/client-s3";
import { GetParameterCommand, SSMClient } from "@aws-sdk/client-ssm";
import { createPresignedPost } from "@aws-sdk/s3-presigned-post";

export default class MatchService {
  public static async getPreSignedUrls(matchId: string, numParts: number) {
    const s3 = new S3Client({});
    const key = matchId; // unique key to identify the asset in S3

    // get bucket name
    const ssm = new SSMClient({});
    const bucketNameParam = await ssm.send(
      new GetParameterCommand({
        Name: "/simdynamx/assets/bucket-name",
      }),
    );
    const bucket = bucketNameParam.Parameter?.Value;

    // initialize upload and get uploadId
    const initUpload = await s3.send(
      new CreateMultipartUploadCommand({
        Bucket: bucket,
        Key: key,
      }),
    );
    const uploadId = initUpload.UploadId;
    if (!uploadId) throw new Error("UploadId is undefined");

    // generate presigned urls for each part
    const presignedUrls = [];
    for (let partNumber = 1; partNumber <= numParts; partNumber++) {
      const { url, fields } = await createPresignedPost(s3, {
        Bucket: "myBucket",
        Key: `${key}-${partNumber}`, // unique key for each part
        Expires: 60, // 1 minute,
        Conditions: [
          ["eq", "$Content-Type", "binary/octet-stream"],
          ["content-length-range", 0, 104857600], // up to 100 MB per part
        ],
      });
      presignedUrls.push({ url, fields });
    }

    return { uploadId, key, presignedUrls };
  }

  /**
   * Call after all parts of an asset have been uploaded to S3.
   * Insert asset metadata into sql database.
   */
  public static async completeUpload(request: CompleteUploadRequest) {
    const { uploadId, key, eTags } = request;

    // ----- insert match metadata into database
    /* const newMatch = {
      ...match,
      match_id: createId(),
      
    }; */

    // await ProjectRepository.createAsset(newMatch);

    // ----- complete upload
    const s3 = new S3Client({});

    // get bucket name
    const ssm = new SSMClient({});
    const bucketNameParam = await ssm.send(
      new GetParameterCommand({
        Name: "/simdynamx/assets/bucket-name",
      }),
    );
    const bucket = bucketNameParam.Parameter?.Value;

    // get all parts
    const parts = eTags.map((eTag, index) => ({
      ETag: eTag,
      PartNumber: index + 1,
    }));

    const { Location } = await s3.send(
      new CompleteMultipartUploadCommand({
        Bucket: bucket,
        Key: key,
        UploadId: uploadId,
        MultipartUpload: {
          Parts: parts,
        },
      }),
    );

    if (!Location) {
      throw new Error("Asset location is undefined");
    }

    return { location: Location };
  }
}
