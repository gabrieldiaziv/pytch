"use client";

import { Button } from "@/app/_components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/app/_components/ui/card";
import { Icons } from "@/app/_components/icons";
import { signIn } from "next-auth/react";
import { useSearchParams } from "next/navigation";

import { getBaseUrl } from "@/utils";
import { MuseoModerno } from "next/font/google";

const museo = MuseoModerno({ subsets: ["latin"] });

const Form = () => {
  const searchParams = useSearchParams();

  const redirectLogin = (
    e: React.FormEvent,
    connection: "google-oauth2" | "github",
  ) => {
    e.preventDefault();

    console.log(connection);

    const res = void signIn(
      "auth0",
      {
        redirect: true,
        callbackUrl: `${getBaseUrl()}`,
      },
      {
        connection,
      },
    );
  };

  const notifications = [
    {
      title: "Your call has been confirmed.",
      description: "1 hour ago",
    },
    {
      title: "You have a new message!",
      description: "1 hour ago",
    },
    {
      title: "Your subscription is expiring soon!",
      description: "2 hours ago",
    },
  ];

  return (
    <div className="flex min-h-[100svh] w-full flex-col">
      <div className="flex h-[100svh] flex-col items-center justify-center">
        <Card className="w-[380px]">
          <CardHeader className="items-center">
            <CardTitle
              className={`text-3xl font-bold tracking-tight ${museo.className} lowercase`}
            >
              pytch
            </CardTitle>
            <CardDescription>Log in or create a Pytch account.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            <div className="grid grid-cols-2 gap-6">
              <Button
                onClick={(e) => redirectLogin(e, "github")}
                variant="outline"
              >
                <Icons.gitHub className="mr-2 h-4 w-4" />
                Github
              </Button>
              <Button
                onClick={(e) => redirectLogin(e, "google-oauth2")}
                variant="outline"
              >
                <Icons.google className="mr-2 h-4 w-4" />
                Google
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Form;
