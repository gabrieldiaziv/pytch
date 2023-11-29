"use client";
// import { useState, useEffect } from "react";
import { getServerSession } from "next-auth";
import { authOptions } from "@/server/auth";

import { Card, CardContent } from "@/app/_components/ui/card";

import axios from "axios";
import React, { useEffect, useState, ChangeEvent } from "react";
import Link from "next/link";

import type { GameMatch } from '@prisma/client';

type AutocompleteProps = {
  items: GameMatch[]; // Assuming items is an array of objects with a name property
  setFilteredItems: (items: { name: string }[]) => void;
  text: string;
  setText: (text: string) => void;
};

const formatDate = (dateString: string): string => {
  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
    day: "numeric",
  };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const Autocomplete: React.FC<AutocompleteProps> = ({ items, setFilteredItems, text, setText }) => {
  const onType = (e: ChangeEvent<HTMLInputElement>) => {
    const searchText = e.target.value;
    setText(searchText);

    setFilteredItems(
      items.filter((item) =>
        item.match.name.toLowerCase().includes(searchText.toLowerCase()),
      ),
    );
  };

  return (
    <div className="w-full flex-col">
      <div className="w-full flex-row">
        <input
          className="w-1/4 border-2 px-3 py-2"
          type="text"
          placeholder="Search"
          onInput={onType}
          value={text}
        />
      </div>
    </div>
  );
};

export default function UserPage() {
  const [matches, setMatches] = useState<GameMatch[]>([]); // State to store matches data


  const [text, setText] = useState("");
  const [filteredItems, setFilteredItems] = useState<GameMatch[]>([]);
  const matchList: JSX.Element[] = [];

  const searchItems =
    filteredItems.length > 0 || text.length > 0 ? filteredItems : matches;

  searchItems.forEach((match, index) => {
    matchList.push(
      <Link
      href={`/dashboard/${match.match.match_id}`}
      key={index}
      style={{ backgroundImage: `url(${match.match.thumbnail_url})` }}
      className="relative flex aspect-video w-full overflow-hidden rounded-lg bg-gray-800 bg-cover duration-300 hover:scale-[101%] md:w-1/2 lg:w-1/3"
    >
      <div className="z-10 flex flex-col gap-1 self-end p-4 text-white">
        <h1 className="text-3xl font-bold">{match.match.name}</h1>
        <div className="flex flex-col gap-1">
          <p className="text-lg">
            {match.match.teamid_home} vs. {match.match.teamid_away}
          </p>
          <p className="text-xs">{formatDate(match.match.date)}</p>
        </div>
      </div>
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-black to-transparent opacity-90"></div>
    </Link>
    );
  });

  useEffect(() => {
    async function fetchData() {
      // const session = await getServerSession(authOptions); // Assuming you need session
      try {
        const response = await axios.get("/api/matches"); // Fetching matches
        setMatches(response.data.matches); // Storing matches in state
      } catch (error) {
        console.error("Error fetching matches data:", error);
      }
    }

    fetchData();
  }, []); // Empty dependency array ensures this runs once on mount

  return (
    <div className="flex h-[100svh] w-full flex-col">
      <div className="flex h-[10%] w-full"></div>
      <div className="flex h-[90%] w-full">
        <div className="flex h-1/2 w-full flex-col gap-6 p-4">
          <h1 className="text-3xl font-semibold">Dashboard</h1>
          <Autocomplete
              items={matches}
              setFilteredItems={setFilteredItems}
              text={text}
              setText={setText}
            />
          <div>
            {matchList}
          </div>
          <div className="flex h-full"></div>
        </div>
      </div>
    </div>
  );
}
