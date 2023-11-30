"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/app/_components/ui/button";
import { api } from "@/trpc/react";

const CustomFrame = ({ url }: { url: string }) => {
  const [frameContent, setFrameContent] = useState("");

  useEffect(() => {
    const fetchHtmlContent = async () => {
      try {
        const response = await fetch(url);

        if (response.ok) {
          const blob = await response.blob();
          const textContent = await new Response(blob).text();
          setFrameContent(textContent);
        } else {
          console.error("Failed to fetch HTML content:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching HTML content:", error);
      }
    };

    void fetchHtmlContent();
  }, [url]);

  return (
    <div>
      <iframe
        title="test"
        srcDoc={frameContent}
        className="w-full h-[500px] rounded-lg"
      ></iframe>
    </div>
  );
};

export default function MatchPage({ params }: { params: { id: string } }) {
  const match = api.match.getMatch.useQuery({ matchId: params.id }).data;
  const vizs = api.match.getVizs.useQuery({ matchId: params.id });

  return (
    <div className="flex h-[100svh] w-full flex-col">
      <div className="flex h-[90%] w-full">
        <div className="flex h-1/2 w-full flex-col gap-6 p-4">
          <div>
            {match ? (
              <div className="flex w-full flex-col gap-3">
                <div className="flex w-full flex-col items-baseline gap-2">
                  <Link href="/dashboard">
                    <Button>Back</Button>
                  </Link>
                  <div className="flex w-full items-baseline justify-between gap-3">
                    <div className="flex items-baseline gap-3">
                      <h1 className="text-3xl font-semibold">
                        {match.name}: {match.team1Name} vs. {match.team2Name}
                      </h1>
                      <p className="text-sm">
                        {match.date?.toLocaleDateString(undefined, {
                          year: "numeric",
                          month: "long",
                          day: "numeric",
                        })}
                      </p>
                    </div>
                    <Link href={`${match.match_json}`}>
                      {" "}
                      <Button>Download Match JSON</Button>
                    </Link>
                  </div>
                </div>

                <div className="flex w-full gap-3 max-md:flex-col">
                  <div className="flex w-full flex-col gap-2 md:w-1/2">
                    <h2 className="font-bold">Labeled Video</h2>
                    <video
                      className="aspect-video w-full overflow-hidden rounded-lg"
                      autoPlay
                      loop
                      muted
                      controls
                    >
                      <source
                        src={match.generated_video ?? ""}
                        type="video/mp4"
                      />
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
                      controls
                    >
                      <source
                        src={match.localization_video ?? ""}
                        type="video/mp4"
                      />
                      <p>Your browser does not support the video tag.</p>
                    </video>
                  </div>
                </div>
                <div className="flex h-full w-full gap-3 max-md:flex-col">
                  <div className="flex w-full flex-col">
                    {vizs.data ? (
                      <div className="flex w-full flex-col gap-3 py-4">
                        {vizs.data.map((match, index) => (
                          <div key={index} className="flex flex-col gap-2 w-auto">
                            <h2 className="font-bold">{match.name}</h2>
                            <h3 className="text-sm">{match.descr}</h3>
                            <CustomFrame url={match.url} />
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div>Getting Matches...</div>
                    )}
                  </div>
                </div>
              </div> // Safely access match properties
            ) : (
              <div className="flex h-[100svh] w-full items-center justify-center">
                Loading match data...
              </div> // Display loading or placeholder
            )}
          </div>
          <div className="flex h-full"></div>
        </div>
      </div>
    </div>
  );
}
