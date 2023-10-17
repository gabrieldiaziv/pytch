import type {
  GetServerSidePropsContext,
  InferGetServerSidePropsType,
} from "next";
import { getProviders, signIn } from "next-auth/react";
import { getServerSession } from "next-auth/next";
import { authOptions } from "~/server/auth";
import Head from "next/head";

import { MuseoModerno } from "next/font/google";

const museo = MuseoModerno({ subsets: ["latin"] });

export default function SignIn({
  providers,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  return (
    <>
      <Head>
        <title>Pytch - Sign In</title>
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
      <main className="flex h-screen w-screen items-center justify-center">
        <div className="flex flex-col py-4 px-16 items-center gap-6">
            <div className="flex flex-col gap-16 items-center">
                <h1 className={`text-5xl font-bold tracking-tight ${museo.className} lowercase`}>pytch</h1>
                <p>Log in or create a Pytch account</p>
            </div>
          {Object.values(providers).map((provider) => (
            <div key={provider.name}>
              <button
                onClick={() => signIn(provider.id)}
                className="rounded-full bg-black px-5 py-2 font-semibold text-white no-underline transition duration-300 hover:bg-gray-500"
              >
                Continue with {provider.name}
              </button>
            </div>
          ))}
        </div>
      </main>
    </>
  );
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const session = await getServerSession(context.req, context.res, authOptions);

  if (session) {
    return { redirect: { destination: "/dashboard" } };
  }

  const providers = await getProviders();

  return {
    props: { providers: providers ?? [] },
  };
}
