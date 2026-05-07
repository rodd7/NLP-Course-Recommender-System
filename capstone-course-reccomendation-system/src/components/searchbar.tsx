"use client";

import { Command, CommandInput } from "@/components/ui/command";
import { Skeleton } from "@/components/ui/skeleton";
import { useEffect, useState } from "react";
import { searchIndex } from "@/app/api/searchIndex";
import { ResultCard } from "@/components/resultCard";

import { getSubjectRecommendedYear } from "@/app/api/recommendedYear";

import dotenv from "dotenv";
import Link from "next/link";

dotenv.config();

interface RecommendedYears {
	[subjectID: string]: number;
}

const getTagsFromOrganisationalName = (
	organisationalName: string,
	availability: string,
	level: string,
	resultType: string,
	highestYear: number,
) => {
	const tags: string[] = [];
	const nameLower = organisationalName.toLowerCase();

	if (/\bengineering\b/.test(nameLower)) tags.push("Engineering");
	if (/\bcommunication\b/.test(nameLower)) tags.push("Communication");
	if (/\beducation\b/.test(nameLower)) tags.push("Education");
	if (/\bbusiness\b/.test(nameLower)) tags.push("Business");
	if (/\bdesign, architecture and building\b/.test(nameLower)) tags.push("DAB");
	if (/\bit\b/.test(nameLower)) tags.push("IT");
	if (/\binformation technology\b/.test(nameLower)) tags.push("IT");
	if (/\bhealth\b/.test(nameLower)) tags.push("Health");
	if (/\blaw\b/.test(nameLower)) tags.push("Law");
	if (/\bscience\b/.test(nameLower)) tags.push("Science");
	if (/\btransdisciplinary\b/.test(nameLower)) tags.push("Transdisciplinary");

	if (availability.toLowerCase().includes("jul")) {
		tags.push("July Session");
	}
	if (availability.toLowerCase().includes("spr")) {
		tags.push("Spring Session");
	}
	if (availability.toLowerCase().includes("aut")) {
		tags.push("Autumn Session");
	}

	if (level.toLowerCase().includes("undergraduate")) {
		tags.push("Undergraduate");
	} else {
		tags.push("Postgraduate");
	}

	tags.push(resultType);

	if (highestYear > 0) {
		highestYear == 1
			? tags.push(highestYear.toString() + "st-Year")
			: highestYear == 2
			? tags.push(highestYear.toString() + "nd-Year")
			: highestYear == 3
			? tags.push(highestYear.toString() + "rd-Year")
			: tags.push(highestYear.toString() + "th-Year");
	}

	return tags;
};

export function Searchbar() {
	const [searchValue, setSearchValue] = useState("");
	const [debouncedSearchValue, setDebouncedSearchValue] = useState(searchValue);
	const [results, setResults] = useState<string | null>(null);
	const [isLoading, setIsLoading] = useState(false); // skeletons
	const [averageConfidenceScore, setAverageConfidenceScore] = useState<
		number | null
	>(null);
	const [recommendedYears, setRecommendedYears] = useState<RecommendedYears>(
		{},
	);

	// debounce result first
	useEffect(() => {
		const debounceTimeout = setTimeout(() => {
			setDebouncedSearchValue(searchValue);
			setAverageConfidenceScore(null);
		}, 1000);

		return () => clearTimeout(debounceTimeout); // cleanup
	}, [searchValue]);

	// then post it
	useEffect(() => {
		const fetchSearchResults = async () => {
			try {
				if (debouncedSearchValue.length > 3) {
					setIsLoading(true); // Start showing skeletons
					const output = await searchIndex(debouncedSearchValue);
					setResults(output);
					setIsLoading(false); // Stop showing skeletons when ready

					if (output != null) {
						const parsedResults = JSON.parse(output);
						const confidenceScores = parsedResults.map(
							(subject: { [x: string]: string }) =>
								Number(parseFloat(subject["Vector Search Score"]).toFixed(5)) *
								100,
						);
						const totalScore = confidenceScores.reduce(
							(acc: number, score: number) => acc + score,
							0,
						);
						const averageScore = totalScore / confidenceScores.length;
						setAverageConfidenceScore(averageScore); // Store the average score

						const subjectIDs = parsedResults.map(
							(subject: { [x: string]: string }) => subject["Subject ID"],
						);
						const recommendedYearsData = await Promise.all(
							subjectIDs.map((subjectID: string) =>
								getSubjectRecommendedYear(parseInt(subjectID)),
							),
						);

						// Create a mapping of subjectID to recommendedYear
						const recommendedYearMap = subjectIDs.reduce(
							(acc: RecommendedYears, subjectID: string, index: number) => {
								acc[subjectID] = recommendedYearsData[index];
								return acc;
							},
							{} as RecommendedYears,
						);

						setRecommendedYears(recommendedYearMap);
					}
				} else {
					setResults(null);
					setIsLoading(false);
				}
			} catch (error) {
				console.error("Error fetching search results:", error);
				setIsLoading(false); // Stop loading in case of error
				setResults(null); // Optionally, clear the results on error
			}
		};

		fetchSearchResults();
	}, [debouncedSearchValue]);

	return (
		<div>
			<Command>
				<CommandInput
					placeholder={"Dynamically search for your University Subject..."}
					value={searchValue || ""}
					onInput={(e) => {
						const target = e.target as HTMLInputElement;
						const value = target.value || "";
						setSearchValue(value);
					}}
				/>
			</Command>

			<div className="flex w-full flex-col overflow-hidden border border-navbar rounded-md text-popover-foreground mt-1">
				{/* Content can be on the left */}
				<div className="flex justify-between items-center p-2 text-navbar">
					{/* Left content (if any) */}
					<p>Some left content here</p>

					{/* Right-aligned confidence score */}
					{averageConfidenceScore && (
						<>
							<span className="ml-auto rounded-md bg-navbar text-white text-sm p-1">
								<b>Avg. Score:</b>{" "}
								<span>{averageConfidenceScore.toFixed(4)}%</span>
							</span>
						</>
					)}
				</div>
			</div>

			<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-5">
				{isLoading && (
					<>
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
						<Skeleton className="w-full h-[200px] rounded-sm bg-navbar p-2 flex flex-col" />
					</>
				)}

				{!isLoading &&
					results != null &&
					JSON.parse(results).map((subject: { [x: string]: string }) => {
						const highestYear =
							recommendedYears[parseInt(subject["Subject ID"])];

						const tags = getTagsFromOrganisationalName(
							subject["subjectOrganisationalName"],
							subject["subjectAvailability"],
							subject["subjectLevel"],
							subject["subjectResultType"],
							highestYear,
						);

						return (
							<Link
								key={subject["Subject ID"]}
								href={`/${subject["Subject ID"]}`}
							>
								<ResultCard
									subjectTitle={subject["Subject Title"]}
									subjectCreditPoints={Number(subject["subjectCreditPoints"])}
									subjectOrganisationalName={
										subject["subjectOrganisationalName"]
									}
									subjectExcerpt={`${subject["Snippet"]}...`}
									subjectConfidenceScore={
										Number(
											parseFloat(subject["Vector Search Score"]).toFixed(5),
										) * 100
									}
									subjectTags={tags} // Pass the generated tags here
									subjectID={subject["Subject ID"]}
								/>
							</Link>
						);
					})}
			</div>
		</div>
	);
}
