import React from "react";
import Link from "next/link";
import { signIn, signOut, useSession } from "next-auth/react";
import { api } from "~/utils/api";

import { MuseoModerno } from "next/font/google";

const museo = MuseoModerno({ subsets: ["latin"] });

const Header: React.FC = () => {
  return (
    <header className="fixed left-0 top-0 w-full bg-white p-4 text-black border-b border-gray-300 z-50">
      <nav className="flex flex-wrap items-center justify-between">
        <div className="mr-6 flex flex-shrink-0 items-center">
          <Link
            href="/"
            className={`text-2xl font-bold tracking-tight ${museo.className} lowercase`}
          >
            Pytch
          </Link>
        </div>
        <div className="flex gap-4 font-medium items-center text-sm">
          <Link href="/api-docs" className="duration-300 hover:text-gray-500">
            API
          </Link>
          <Link href="/help" className="duration-300 hover:text-gray-500">
            Help
          </Link>
          <AuthShowcase />
        </div>
      </nav>
    </header>
  );
};

export default Header;

function AuthShowcase() {
    const { data: sessionData } = useSession();
  
    const { data: secretMessage } = api.example.getSecretMessage.useQuery(
      undefined, // no input
      { enabled: sessionData?.user !== undefined }
    );
  
    return (
      <div className="flex flex-col items-center justify-center gap-4 h-8">
        <button
          className="rounded-full px-5 py-2 font-semibold text-white no-underline transition bg-black hover:bg-gray-500 duration-300"
          onClick={sessionData ? () => void signOut() : () => void signIn()}
        >
          {sessionData ? "Sign Out" : "Sign In"}
        </button>
      </div>
    );
  }