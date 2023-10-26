"use client";

import { signIn } from "next-auth/react";
import { Icons } from "@/components/icons";
import { useSearchParams } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

import { MuseoModerno } from "next/font/google";

const museo = MuseoModerno({ subsets: ["latin"] });

const Form = () => {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams?.get("callbackUrl") || "/";

  const onDiscordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await signIn("discord", {
      redirect: false,
      callbackUrl,
    });
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
              <Button onClick={onDiscordSubmit} variant="outline">
                <Icons.gitHub className="mr-2 h-4 w-4" />
                Github
              </Button>
              <Button variant="outline">
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
