"use client";

import { signIn, signOut, useSession } from "next-auth/react";
import Link from "next/link";
import React from "react";

import { Button } from "@/app/_components/ui/button";

import { UserNav } from "@/app/_components/ui/avatar-nav";
import { ModeToggle } from "@/app/_components/ui/mode-toggle";
import { MuseoModerno } from "next/font/google";

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
          {session?.user ? (
            <Link href="/upload" className="duration-300 hover:text-gray-500">
              Upload
            </Link>
          ) : null}
          <Link href="/api-docs" className="duration-300 hover:text-gray-500">
            API
          </Link>
          <Link href="/help" className="duration-300 hover:text-gray-500">
            Help
          </Link>
          {session?.user ? (
            <UserNav session={session} />
          ) : (
            <Button
              variant="default"
              onClick={
                session?.user
                  ? () => signOut({ redirect: true, callbackUrl: "/" })
                  : () => signIn()
              }
            >
              Sign In
            </Button>
          )}
          <ModeToggle />
        </div>
      </nav>
    </header>
  );
};

export default Header;
