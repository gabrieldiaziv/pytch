import Link from "next/link";

import { buttonVariants } from "@/app/_components/ui/button";
import { getServerAuthSession } from "@/server/auth";

export default function Home() {
  // const hello = await api.post.hello.query({ text: "from tRPC" });

  return (
    <main className="flex min-h-screen flex-col items-center">
      <section className="relative flex h-[100vh] w-screen  items-center justify-start overflow-hidden">
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
  );
}

async function AuthShowcase() {
  const session = await getServerAuthSession();

  return (
    <Link
      className={buttonVariants({ variant: "secondary" }) + " w-max"}
      href={session?.user ? "/dashboard" : "/auth/signin"}
    >
      {session?.user ? "Go to Dashboard" : "Get Started"}
    </Link>
  );
}
