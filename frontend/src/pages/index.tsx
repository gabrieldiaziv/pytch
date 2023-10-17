import { signIn, signOut, useSession } from "next-auth/react";
import Head from "next/head";
import Link from "next/link";

import { api } from "~/utils/api";

export default function Home() {
  // const hello = api.example.hello.useQuery({ text: "from tRPC" });
  const { data: sessionData } = useSession();

  const { data: secretMessage } = api.example.getSecretMessage.useQuery(
    undefined, // no input
    { enabled: sessionData?.user !== undefined },
  );

  return (
    <>
      <Head>
        <title>Pytch - Computer Vision for Soccer Analytics</title>
        <meta
          name="description"
          content="Pytch is a cutting-edge platform leveraging computer vision for in-depth soccer analytics. Dive deep into match data, player performances, and more with Pytch."
        />
        <meta
          name="keywords"
          content="soccer, football, analytics, computer vision, Pytch, match analysis, player statistics, sports technology"
        />
        <meta
          name="author"
          content="Gabriel Diaz, Ryan Kutz, Ryan Son, Joseph Quismorio, Shurui Xu, Anthony Pasala"
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="flex min-h-screen flex-col items-center bg-white">
        <section className="relative flex h-[80vh] w-screen items-end justify-start">
          <video
            src="/assets/e6017ed8-a551-4d7e-b074-2d34c14df115.mp4"
            autoPlay
            muted
            loop
            className="absolute inset-0 h-full w-full object-cover"
          ></video>
          <div className="absolute -inset-px bg-gray-900/50"></div>
          <div className="absolute -inset-px bg-gradient-to-b from-transparent via-transparent to-gray-900"></div>
          <div className="z-10 flex flex-col gap-4 p-6 text-white md:w-2/5">
            <h1 className="text-5xl font-bold max-md:text-4xl md:w-3/4">
              Advanced soccer stats, all for free.
            </h1>
            <p className="text-base max-md:text-sm">
              Get computer vision-powered insights on any football match and
              elevate your game analysis like never before.
            </p>
            <AuthShowcase />
          </div>
        </section>
      </main>
    </>
  );
}

function AuthShowcase() {
  const { data: sessionData } = useSession();

  const { data: secretMessage } = api.example.getSecretMessage.useQuery(
    undefined, // no input
    { enabled: sessionData?.user !== undefined },
  );

  return (
    <Link
      className="w-max rounded-full px-5 py-2 font-semibold text-white no-underline transition bg-black hover:bg-gray-500 duration-300"
      href={sessionData ? "/dashboard" : "/auth/signin"}
    >
      {sessionData ? "Go to Dashboard" : "Get Started"}
    </Link>
  );
}
