"use client";

import { env } from "@/env.mjs";
import { clientErrorHandler, cn } from "@/lib/utils";
import axios from "axios";
import { format } from "date-fns";
import { ArrowRight, Calendar as CalendarIcon } from "lucide-react";
import { useSession } from "next-auth/react";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { useToast } from "@/app/_components/ui/use-toast";

import { Button } from "@/app/_components/ui/button";
import { Calendar } from "@/app/_components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/app/_components/ui/popover";
import { api } from "@/trpc/react";
import { createId } from "@paralleldrive/cuid2";
import { Input } from "@/app/_components/ui/input";
import { Label } from "@/app/_components/ui/label";
import { ToastAction } from "../_components/ui/toast";
import { useRouter } from "next/navigation";

type MyDropzoneProps = {
  isUsable: boolean;
  matchName: string;
  team1Name: string;
  team2Name: string;
  matchDate: Date;
  clearInputs?: () => void;
};

function MyDropzone({
  isUsable,
  matchName,
  team1Name,
  team2Name,
  matchDate,
  clearInputs
}: MyDropzoneProps) {
  const { toast } = useToast();
  const router = useRouter();
  const { data: session } = useSession();
  const { mutate: insertMatch } = api.match.insertMatch.useMutation({
    onSuccess: () => {
      toast({
        title: "Processing match...",
        description: "Go to dashboard for results",
        action: (
          <ToastAction altText="Link to dashboard" onClick={
            () => {
              void router.push("/dashboard");
            }
          }><ArrowRight /></ToastAction>
        ),
        duration: 5000
      })

      if (clearInputs) {
        clearInputs();
      }
    },
    onError: (err) => {
      clientErrorHandler(err, toast);
    },
  });

  const onDrop = useCallback(
    <T extends File>(acceptedFiles: T[]) => {
      if (!session) {
        return;
      }
      const matchId = createId();

      insertMatch({
        matchId,
        matchName,
        team1Name,
        team2Name,
        matchDate,
      });

      // send files to backend

      acceptedFiles.forEach((file) => {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("matchId", matchId);
        formData.append("team1Name", team1Name);
        formData.append("team2Name", team2Name);

        axios
          .post(env.NEXT_PUBLIC_FLASK_URL + "/detect", formData, {
            headers: {
              Authorization: `Bearer ${session.idToken}`,
            },
          })
          .then((response) => {
            const url = window.URL.createObjectURL(response.data as Blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "files.zip"; // or any other extension
            document.body.appendChild(a);
            a.click();
            a.remove();
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      });
    },
    [insertMatch, matchDate, matchName, session, team1Name, team2Name],
  );
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "video/*": [".mp4", ".avi", ".mkv", ".flv"],
    },
    onDrop,
  });

  if (!session || !isUsable) {
    return (
      <div className="rounded-md border border-neutral-200 bg-gray-100 p-16 text-center text-black">
        <div className="flex justify-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="black"
            className=" h-12 w-12"
          >
            <path
              fillRule="evenodd"
              d="M10.5 3.75a6 6 0 00-5.98 6.496A5.25 5.25 0 006.75 20.25H18a4.5 4.5 0 002.206-8.423 3.75 3.75 0 00-4.133-4.303A6.001 6.001 0 0010.5 3.75zm2.03 5.47a.75.75 0 00-1.06 0l-3 3a.75.75 0 101.06 1.06l1.72-1.72v4.94a.75.75 0 001.5 0v-4.94l1.72 1.72a.75.75 0 101.06-1.06l-3-3z"
              clipRule="evenodd"
            />
          </svg>
        </div>
        <p className="text-black">Dropzone</p>
        <p>
          {!session
            ? "Sign in to upload files."
            : "Fill in all below fields before uploading."}
        </p>
      </div>
    );
  }

  return (
    <div
      className="cursor-pointer rounded-md border border-neutral-200 bg-gray-100 p-16 text-center text-black"
      {...getRootProps()}
    >
      {/* For menu bar later ?? */}
      {/* <div className="self-end text-center w-4/5 p-16 mt-10 bg-gray-100 border rounded-md border-neutral-200" {...getRootProps()}>  */}

      <div className="flex justify-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="#02b946"
          className=" h-12 w-12"
        >
          <path
            fillRule="evenodd"
            d="M10.5 3.75a6 6 0 00-5.98 6.496A5.25 5.25 0 006.75 20.25H18a4.5 4.5 0 002.206-8.423 3.75 3.75 0 00-4.133-4.303A6.001 6.001 0 0010.5 3.75zm2.03 5.47a.75.75 0 00-1.06 0l-3 3a.75.75 0 101.06 1.06l1.72-1.72v4.94a.75.75 0 001.5 0v-4.94l1.72 1.72a.75.75 0 101.06-1.06l-3-3z"
            clipRule="evenodd"
          />
        </svg>
      </div>

      <input {...getInputProps()} />
      <p className="text-[#02b946]">Dropzone</p>
      {isDragActive ? (
        <p>Drop the files here (mp4, avi, mkv, and flv).</p>
      ) : (
        <p>Click to add files (mp4, avi, mkv, and flv).</p>
      )}
    </div>
  );
}

export default function UploadPage() {
  const [team1Name, setTeam1Name] = useState("");
  const [team2Name, setTeam2Name] = useState("");
  const [matchName, setMatchName] = useState("");
  const [date, setDate] = useState<Date>();

  const clearInputs = useCallback(() => {
    setTeam1Name("");
    setTeam2Name("");
    setMatchName("");
    setDate(undefined);
  }, []);

  const allFieldsFilled =
    team1Name && team2Name && matchName && date ? true : false;

  return (
    <div className="flex h-full w-full flex-col">
      <div className="flex h-full w-full">
        <div className="no-scrollbar flex h-full w-full flex-col gap-6 overflow-y-scroll p-4">
          <h1 className="text-3xl font-semibold">Upload</h1>
          <div className="flex w-full gap-3">
            <div className="grid w-full max-w-[50%] items-center gap-1.5">
              <Label htmlFor="team1">Team 1</Label>
              <Input
                type="text"
                id="team1"
                value={team1Name}
                onChange={(e) => setTeam1Name(e.target.value)}
                placeholder="Tottenham Hotspur F.C."
              />
            </div>
            <div className="grid w-full max-w-[50%] items-center gap-1.5">
              <Label htmlFor="team2">Team 2</Label>
              <Input
                type="text"
                id="team2"
                value={team2Name}
                onChange={(e) => setTeam2Name(e.target.value)}
                placeholder="Arsenal F.C."
              />
            </div>
          </div>
          <div className="flex w-full gap-3 items-center">
            <div className="grid w-full max-w-[75%] items-center gap-1.5">
              <Label htmlFor="matchName">Match Name</Label>
              <Input
                type="text"
                id="matchName"
                value={matchName}
                onChange={(e) => setMatchName(e.target.value)}
                placeholder="North London Derby"
              />
            </div>
            <div className="grid w-full max-w-[25%] items-center gap-1.5">
              <Label htmlFor="matchDate">Match Date</Label>
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant={"outline"}
                    className={cn(
                      "justify-start text-left font-normal",
                      !date && "text-muted-foreground",
                    )}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {date ? format(date, "PPP") : <span>Pick a date</span>}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                  <Calendar
                    mode="single"
                    selected={date}
                    onSelect={setDate}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
            </div>
          </div>
          <MyDropzone
            isUsable={allFieldsFilled}
            matchName={matchName}
            team1Name={team1Name}
            team2Name={team2Name}
            matchDate={date ?? new Date()}
            clearInputs={clearInputs}
          />
        </div>
      </div>
    </div>
  );
}
