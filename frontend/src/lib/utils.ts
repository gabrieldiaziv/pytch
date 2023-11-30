import { type AppRouter } from "@/server/api/root";
import { type TRPCClientErrorLike } from "@trpc/client";
import { clsx, type ClassValue } from "clsx";
import { toast } from "react-hot-toast";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * trpc client error handler
 */
export function clientErrorHandler(err: TRPCClientErrorLike<AppRouter>) {
  if (err.data?.zodError) {
    const msgContent = err.data.zodError.fieldErrors.content;
    if (msgContent?.[0]) toast.error(msgContent[0]);
  } else {
    toast.error(err.message);
  }
}
