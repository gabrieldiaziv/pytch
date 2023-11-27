"use client";
// import { useState, useEffect } from "react";
import { getServerSession } from "next-auth";
import { authOptions } from "@/server/auth";

import {
  Card,
  CardContent,
} from "@/app/_components/ui/card";

import axios from "axios";
import React, { useEffect, useState } from 'react';
import Link from "next/link";

const formatDate = (dateString: string): string => {
  const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

export default function UserPage() {
  const [matches, setMatches] = useState([]); // State to store matches data

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
    <div className="flex flex-col w-full h-[100svh]">
      <div className="flex w-full h-[10%]">

      </div>
      <div className="flex w-full h-[90%]">
        <div className="flex flex-col w-full h-1/2 p-4 gap-6">
          <h1 className="text-3xl font-semibold">Dashboard</h1>
          <div>
          {matches.map((match, index) => (
            <Link
              href={`/dashboard/${match.match.match_id}`}
              key={index}
              style={{ backgroundImage: `url(${match.match.thumbnail_url})` }}
              className="flex aspect-video w-1/3 bg-cover bg-gray-100 rounded-lg duration-300 hover:scale-[101%]"
            >
              <div className="self-end p-2 text-white flex flex-col gap-1">
                <h1 className="font-bold text-2xl">{match.match.name}</h1>
                <p className="text-sm">{match.match.teamid_home} vs. {match.match.teamid_away}</p>
                <p className="text-sm">{formatDate(match.match.date)}</p>
              </div>
            </Link>
            ))}
          </div>
          <div className="flex h-full">
          </div>
        </div>
      </div>
    </div>
  );
}
