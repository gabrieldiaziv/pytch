import type { UseSessionOptions } from "next-auth/react";
import { signIn, signOut, useSession } from "next-auth/react";
import { useMemo } from "react";

type AuthStatus = ReturnType<typeof useSession>["status"] | "activate";

// TODO: prompt user to change username if they are an INITIAL_USER
export default function useAuth(args?: UseSessionOptions<boolean>) {
  const { data: session, status, update } = useSession(args);

  const authStatus: AuthStatus = useMemo(() => {
    if (session) {
      if (session.user.type === "INITIAL_USER") {
        // user didn't update their username to something unique yet
        return "activate";
      }
    }

    return status;
  }, [status, session]);

  return { session, authStatus, updateSession: update, signIn, signOut };
}
