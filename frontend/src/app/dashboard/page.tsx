"use client";
// import { useState, useEffect } from "react";

import Link from "next/link";
import React, { useState, type ChangeEvent } from "react";

import { api } from "@/trpc/react";
import type { GameMatch } from "@prisma/client";

type AutocompleteProps = {
  items: GameMatch[]; // Assuming items is an array of objects with a name property
  setFilteredItems: (items: GameMatch[]) => void;
  text: string;
  setText: (text: string) => void;
};

const Autocomplete: React.FC<AutocompleteProps> = ({
  items,
  setFilteredItems,
  text,
  setText,
}) => {
  const onType = (e: ChangeEvent<HTMLInputElement>) => {
    const searchText = e.target.value;
    setText(searchText);

    setFilteredItems(
      items.filter((item) =>
        item.name.toLowerCase().includes(searchText.toLowerCase()),
      ),
    );
  };

  return (
    <input
      className="border-2 px-3 py-2 w-1/4"
      type="text"
      placeholder="Search"
      onInput={onType}
      value={text}
    />
  );
};

export default function UserPage() {
  const [text, setText] = useState("");
  const [filteredItems, setFilteredItems] = useState<GameMatch[]>([]);
  const matchList: JSX.Element[] = [];

  const matches = api.match.getUserMatches.useQuery().data ?? [];

  const searchItems =
    filteredItems.length > 0 || text.length > 0 ? filteredItems : matches;

  searchItems.forEach((match, index) => {
    matchList.push(
      <Link
        href={`/dashboard/${match.match_id}`}
        key={index}
        style={{ backgroundImage: `url(${match.thumbnail_url})` }}
        className="relative flex aspect-video w-full overflow-hidden rounded-lg bg-gray-800 bg-cover duration-300 hover:scale-[101%] md:w-1/2 lg:w-1/3"
      >
        <div className="z-10 flex flex-col gap-1 self-end p-4 text-white">
          <h1 className="text-3xl font-bold">{match.name}</h1>
          <div className="flex flex-col gap-1">
            <p className="text-lg">
              {match.team1Name} vs. {match.team2Name}
            </p>
            <p className="text-xs">
              {match.date?.toLocaleDateString(undefined, {
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </p>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-black to-transparent opacity-90"></div>
      </Link>,
    );
  });

  return (
    <div className="flex flex-col gap-6 p-4">
      <h1 className="text-3xl font-semibold">Dashboard</h1>
      <Autocomplete
        items={matches}
        setFilteredItems={setFilteredItems}
        text={text}
        setText={setText}
      />
      <div className="flex flex-wrap gap-5">{matchList}</div>
    </div>
  );
}
