import React, { useState, useEffect } from "react";
import Link from "next/link";

function Error() {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Using window inside useEffect ensures it's only called client-side
    const query = new URLSearchParams(window.location.search);
    setError(query.get("error"));
  }, []);

  return (
    <div className="flex h-screen w-screen items-center justify-center">
      <div className="flex w-[36rem] flex-col gap-6 p-10 items-center">
        <h1 className="max-md:text-2xl text-3xl font-bold">Uh oh.</h1>
        <p className="max-md:text-sm text-base text-center">
          We&apos;ve encountered an error... {""}
          {error === "Configuration"
            ? "our settings seem to have gotten a bit muddled."
            : ""}
          {error === "Authentication"
            ? "we had a bit of trouble recognizing your credentials."
            : ""}
          {error === "Authorization"
            ? "not all who wander are lost, but this page might be off-limits."
            : ""}
          {error === "Server" ? "our server is rather overwhelmed at the moment." : ""} (Probably Miguel&apos;s fault)
          <br />
          <br />
          We understand that this can be frustrating, and we apologize for the
          inconvenience. Rest assured, our team is on it!
        </p>
        <Link
          href="/"
          className="w-max rounded-full bg-black px-5 py-2 font-semibold text-white no-underline transition duration-300 hover:bg-gray-500"
        >
          Go home
        </Link>
      </div>
    </div>
  );
}

export default Error;
