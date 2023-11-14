"use client";

import { Card, CardContent } from "@/app/_components/ui/card";
import { env } from "@/env.mjs";
import axios from "axios";
import { useSession } from "next-auth/react";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

function MyDropzone() {
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

  if (!session) {
    return (
      <div
        className="rounded-md border border-neutral-200 bg-gray-100 p-16 text-center text-black"
        {...getRootProps()}
      >
        <div className="flex justify-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="purple"
            className=" h-12 w-12"
          >
            <path
              fillRule="evenodd"
              d="M10.5 3.75a6 6 0 00-5.98 6.496A5.25 5.25 0 006.75 20.25H18a4.5 4.5 0 002.206-8.423 3.75 3.75 0 00-4.133-4.303A6.001 6.001 0 0010.5 3.75zm2.03 5.47a.75.75 0 00-1.06 0l-3 3a.75.75 0 101.06 1.06l1.72-1.72v4.94a.75.75 0 001.5 0v-4.94l1.72 1.72a.75.75 0 101.06-1.06l-3-3z"
              clipRule="evenodd"
            />
          </svg>
        </div>
        <p className="text-[#800080]">Dropzone</p>
        <p>Sign in to upload files</p>
      </div>
    );
  }

  return (
    <div
      className="rounded-md border border-neutral-200 bg-gray-100 p-16 text-center text-black"
      {...getRootProps()}
    >
      {/* For menu bar later ?? */}
      {/* <div className="self-end text-center w-4/5 p-16 mt-10 bg-gray-100 border rounded-md border-neutral-200" {...getRootProps()}>  */}

      <div className="flex justify-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="purple"
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
      <p className="text-[#800080]">Dropzone</p>
      {isDragActive ? (
        <p>Drop the files here ...</p>
      ) : (
        <p>Click to add files or drop just about anything on the Board...</p>
      )}
    </div>
  );
}

function Autocomplete({ items, setFilteredItems, text, setText }) {
  const onType = (e) => {
    const searchText = e.target.value;
    setText(e.target.value);

    setFilteredItems((prevFilteredItems) =>
      items.filter((item) =>
        item.toLowerCase().includes(searchText.toLowerCase()),
      ),
    );
    //console.log(searchText);
  };

  return (
    <div className="w-full flex-col">
      <div className="w-full flex-row">
        <input
          className="w-1/4 border-2 px-3 py-2"
          type="text"
          placeholder={"Search"}
          onInput={onType}
          value={text}
        ></input>
      </div>
    </div>
  );
}

export default function UploadPage() {
  const items = [
    "test",
    "eggs",
    "bread",
    "bread",
    "bread",
    "bread",
    "bread",
    "breathe",
  ];
  const [text, setText] = useState("");
  const [filteredItems, setFilteredItems] = useState([]);
  const itemList = [];

  const searchItems =
    filteredItems.length > 0 || text.length > 0 ? filteredItems : items;

  searchItems.forEach((item, index) => {
    itemList.push(
      <Card
        key={index}
        style={{ backgroundImage: `url(${"/assets/logopytch.png"})` }}
        className="flex h-4/5 w-[335px] flex-none bg-gray-100"
      >
        <CardContent className="self-end p-2 text-black">{item}</CardContent>
      </Card>,
    );
  });

  return (
    <div className="flex h-[100svh] w-full flex-col">
      <div className="flex h-[10%] w-full"></div>
      <div className="flex h-[90%] w-full">
        <div className="no-scrollbar flex h-full w-full flex-col gap-6 overflow-y-scroll p-4 px-20">
          <MyDropzone />
          <div className="flex">
            <Autocomplete
              items={items}
              setFilteredItems={setFilteredItems}
              text={text}
              setText={setText}
            />
          </div>

          <div className="flex h-full flex-wrap gap-3">{itemList}</div>
        </div>
      </div>
    </div>
  );
}
