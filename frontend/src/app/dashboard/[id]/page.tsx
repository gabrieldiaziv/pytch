"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";
import { Button } from "@/app/_components/ui/button";

const formatDate = (dateString: string): string => {
  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
    day: "numeric",
  };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

export default function MatchPage({ params }: { params: { id: string } }) {
  const [match, setMatch] = useState<any>(null); // State to store match data

  useEffect(() => {
    async function fetchData() {
      // const session = await getServerSession(authOptions); // Uncomment if needed
      try {
        const response = await axios.get(`/api/matches/${params.id}`);
        setMatch(response.data.match); // Storing match in state
      } catch (error) {
        console.error("Error fetching match data:", error);
      }
    }

    fetchData();
  }, [params.id]); // Include params.id in the dependency array

  return (
    <div className="flex h-[100svh] w-full flex-col">
      <div className="flex h-[10%] w-full"></div>
      <div className="flex h-[90%] w-full">
        <div className="flex h-1/2 w-full flex-col gap-6 p-4">
          <div>
            {match ? (
              <div className="flex w-full flex-col gap-3">
                <div className="flex w-full flex-col items-baseline gap-2">
                  <Link href="/dashboard">
                    <Button>Back</Button>
                  </Link>
                  <div className="flex w-full items-baseline gap-3">
                    <h1 className="text-3xl font-semibold">
                      {match.name}: {match.teamid_home} vs. {match.teamid_away}
                    </h1>
                    <p className="text-sm">{formatDate(match.date)}</p>
                  </div>
                </div>

                <div className="flex w-full gap-3 max-md:flex-col">
                  <div className="flex w-full flex-col gap-2 md:w-1/2">
                    <h2 className="font-bold">Labelled Video</h2>
                    <video
                      className="aspect-video w-full overflow-hidden rounded-lg"
                      autoPlay
                      loop
                      muted
                    >
                      <source
                        src="https://pytchtestbucket.s3.amazonaws.com/MATCH_ID_134-label.mp4"
                        type="video/mp4"
                      />
                      {/* <source src={match.generated_video} type="video/mp4" /> */}
                      <p>Your browser does not support the video tag.</p>
                    </video>
                  </div>

                  <div className="flex w-full flex-col gap-2 md:w-1/2">
                    <h2 className="font-bold">Localized Field</h2>
                    <video
                      className="aspect-video w-full overflow-hidden rounded-lg"
                      autoPlay
                      loop
                      muted
                    >
                      <source
                        src="https://pytchtestbucket.s3.amazonaws.com/MATCH_ID_134-2d.mp4"
                        type="video/mp4"
                      />
                      {/* <source src={match.localization_video} type="video/mp4" /> */}
                      <p>Your browser does not support the video tag.</p>
                    </video>
                  </div>
                </div>
              </div> // Safely access match properties
            ) : (
              <div>Loading match data...</div> // Display loading or placeholder
            )}
          </div>
          <div className="flex h-full"></div>
        </div>
      </div>
    </div>
  );
}
