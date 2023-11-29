"use client";

import { Card, CardContent } from "@/app/_components/ui/card";
import { env } from "@/env.mjs";
import axios from "axios";
import { useSession } from "next-auth/react";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

type MyDropzoneProps = {
  isUsable: boolean;
};

function MyDropzone({ isUsable }: MyDropzoneProps) {
  const { data: session } = useSession();

  const onDrop = useCallback(
    <T extends File>(acceptedFiles: T[]) => {
      if (!session) {
        return;
      }

      acceptedFiles.forEach((file) => {
        const formData = new FormData();
        formData.append("file", file);

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
    [session],
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
        <p>{!session ? "Sign in to upload files." : "Fill in all below fields before uploading."}</p>
      </div>
    );
  }

  return (
    <div
      className="rounded-md border border-neutral-200 bg-gray-100 p-16 text-center text-black cursor-pointer"
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

  const allFieldsFilled = team1Name && team2Name && matchName;

  return (
    <div className="flex h-[100svh] w-full flex-col">
      <div className="flex h-[10%] w-full"></div>
      <div className="flex h-[90%] w-full">
        <div className="no-scrollbar flex h-full w-full flex-col gap-6 overflow-y-scroll p-4">
          <MyDropzone isUsable={allFieldsFilled} />
          <div className="flex w-full gap-3">
            <input
              className="w-full border-2 px-3 py-2"
              type="text"
              placeholder={"Team 1 Name"}
              value={team1Name}
              onChange={(e) => setTeam1Name(e.target.value)}
            />
            <input
              className="w-full border-2 px-3 py-2"
              type="text"
              placeholder={"Team 2 Name"}
              value={team2Name}
              onChange={(e) => setTeam2Name(e.target.value)}
            />
            <input
              className="w-full border-2 px-3 py-2"
              type="text"
              placeholder={"Match Name"}
              value={matchName}
              onChange={(e) => setMatchName(e.target.value)}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
