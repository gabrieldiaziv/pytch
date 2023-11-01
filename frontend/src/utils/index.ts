import { env } from "@/env.mjs";

export const getBaseUrl = () => {
  return env.NEXT_PUBLIC_WEB_URL;
};
