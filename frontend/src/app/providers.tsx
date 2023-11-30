"use client";

import { SessionProvider } from "next-auth/react";
import { Next13ProgressBar } from "next13-progressbar";

type Props = {
  children?: React.ReactNode;
};

export const Providers = ({ children }: Props) => {
  return (
    <SessionProvider>
      <Next13ProgressBar
        height="4px"
        color="#03fc1c"
        options={{ showSpinner: false }}
        showOnShallow
      />
      {children}
    </SessionProvider>
  );
};
