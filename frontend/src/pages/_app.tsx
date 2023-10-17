import { type Session } from "next-auth";
import { SessionProvider } from "next-auth/react";
import { type AppType } from "next/app";
import { Kumbh_Sans }  from "next/font/google"

import Header from "~/components/ui/header";

import { api } from "~/utils/api";

import "~/styles/globals.css";

const lora = Kumbh_Sans({ subsets: ['latin'] })

const MyApp: AppType<{ session: Session | null }> = ({
  Component,
  pageProps: { session, ...pageProps },
}) => {
  return (
    <main className={`${lora.className} tracking-wide`}>

        <SessionProvider session={session}>
          <Header />
          <Component {...pageProps} />
        </SessionProvider>

    </main>
  );
};

export default api.withTRPC(MyApp);
