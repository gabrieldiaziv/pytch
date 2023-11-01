import { z } from "zod";

export const TeamSchema = z.object({
  id: z.string(),
  name: z.string(),
  league: z.string().optional(),
});

export const MatchSchema = z.object({
  user_id: z.string(),
  name: z.string().optional(),
  teamHome: TeamSchema,
  teamAway: TeamSchema,
  date: z.string().optional(),
});

/**
 * Schema for completing a multipart upload of a match to S3 and updating the database
 */
export const CompleteUploadSchema = z.object({
  match: MatchSchema,
  // upload info
  uploadId: z.string(),
  key: z.string(),
  eTags: z.array(z.string()),
});
export type CompleteUploadRequest = z.infer<typeof CompleteUploadSchema>;
