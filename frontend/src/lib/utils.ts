import { type useToast } from "@/app/_components/ui/use-toast";
import { type AppRouter } from "@/server/api/root";
import { type TRPCClientErrorLike } from "@trpc/client";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * trpc client error handler
 */
export function clientErrorHandler(
  err: TRPCClientErrorLike<AppRouter>,
  toast: ReturnType<typeof useToast>["toast"],
) {
  if (err.data?.zodError) {
    const msgContent = err.data.zodError.fieldErrors.content;
    if (msgContent?.[0])
      toast({
        title: "Error",
        description: msgContent[0],
        duration: 5000,
      });
  } else {
    toast({
      title: "Error",
      description: err.message,
      duration: 5000,
    });
  }
}
