"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";

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
              <div>
                <h1 className="text-3xl font-semibold">{match.name}</h1>
                <video className="aspect-video w-[500px]" autoPlay loop muted>
                  <source src={match.localization_video} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
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
