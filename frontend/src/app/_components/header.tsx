"use client";

import React from "react";
import Link from "next/link";
import { signIn, signOut, useSession } from "next-auth/react";

import { Button } from "@/components/ui/button"

import { MuseoModerno } from "next/font/google";
import { ModeToggle } from "@/components/ui/mode-toggle";

const museo = MuseoModerno({ subsets: ["latin"] });

const Header: React.FC = () => {
  const { data: session, status } = useSession();
  return (
    <header className="fixed left-0 top-0 z-50 w-full border-b bg-inherit p-4">
      <nav className="flex flex-wrap items-center justify-between">
        <div className="mr-6 flex flex-shrink-0 items-center">
          <Link
            href="/"
            className={`text-2xl font-bold tracking-tight ${museo.className} lowercase`}
          >
            Pytch
          </Link>
        </div>
        <div className="flex items-center gap-4 text-sm font-medium">
          <Link href="/api-docs" className="duration-300 hover:text-gray-500">
            API
          </Link>
          <Link href="/help" className="duration-300 hover:text-gray-500">
            Help
          </Link>
          <Button
            variant="default"
            // className="rounded-full bg-black px-5 py-2 font-semibold text-white no-underline transition duration-300 hover:bg-gray-500"
            onClick={
              session?.user
                ? () => signOut({ redirect: true, callbackUrl: "/" })
                : () => signIn()
            }
          >
            {session?.user ? "Sign Out" : "Sign In"}
          </Button>
          <ModeToggle />
        </div>
      </nav>
    </header>
  );
};

export default Header;
