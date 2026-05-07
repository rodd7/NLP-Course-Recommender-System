"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Navbar } from "@/components/navbar";
import { getSubjectData } from "../api/subjectData";

interface Subject {
	_id: string;
	subjectID: number;
	subjectTitle: string;
	subjectLink: string;
	subjectAvailability: string;
	subjectCreditPoints: number;
	subjectOrganisationalName: string;
	subjectLevel: string;
	subjectResultType: string;
	subjectDescription: string;
	subjectSLO: string;
	subjectCILO: string;
	subjectStrategy: string;
	subjectContent: string;
	subjectAssessment: string;
	subjectRawText: string;
	subjectEmbedding: string;
	descriptiveTags: string[];
	contextTags: string[];
}

export default function SubjectPage() {
	const params = useParams();
	const subjectID = Array.isArray(params?.subjectID)
		? params.subjectID[0]
		: params?.subjectID;

	const [subjectData, setSubjectData] = useState<Subject | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		const fetchSubjectData = async () => {
			if (subjectID) {
				try {
					setLoading(true);
					setError(null);

					const data = await getSubjectData(Number(subjectID));

					setSubjectData(data && data.length > 0 ? data[0] : null);
				} catch (err) {
					setError("Failed to fetch subject data.");
					console.error("Error fetching subject data:", err);
				} finally {
					setLoading(false);
				}
			}
		};

		fetchSubjectData();
	}, [subjectID]);

	if (loading) {
		return (
			<div>
				<Navbar />
				<p>Loading...</p>
			</div>
		);
	}

	if (error) {
		return (
			<div>
				<Navbar />
				<p>{error}</p>
			</div>
		);
	}

	return (
		<div>
			<Navbar />
			{subjectData ? (
				<div>
					<h1>{subjectData.subjectTitle}</h1>
					<p>
						<strong>Subject ID:</strong> {subjectData.subjectID}
					</p>
					<p>
						<strong>Subject Link:</strong> {subjectData.subjectLink}
					</p>
					<p>
						<strong>Subject Organisation Name:</strong>{" "}
						{subjectData.subjectOrganisationalName}
					</p>
					<p>
						<strong>subjectLevel :</strong> {subjectData.subjectLevel}
					</p>
					<p>
						<strong>subjectResultType :</strong> {subjectData.subjectResultType}
					</p>

					<p>
						<strong>subjectSLO :</strong> {subjectData.subjectSLO}
					</p>

					<p>
						<strong>subjectCILO :</strong> {subjectData.subjectCILO}
					</p>
					<p>
						<strong>subjectStrategy :</strong> {subjectData.subjectStrategy}
					</p>

					<p>
						<strong>subjectContent :</strong> {subjectData.subjectContent}
					</p>

					<p>
						<strong>subjectAssessment :</strong> {subjectData.subjectAssessment}
					</p>

					<p>
						<strong>Subject Description:</strong>{" "}
						{subjectData.subjectDescription}
					</p>
					<p>
						<strong>Credit Points:</strong> {subjectData.subjectCreditPoints}
					</p>
					<p>
						<strong>Availability:</strong> {subjectData.subjectAvailability}
					</p>
					<p>
						<strong>Descriptive Tags: </strong>
						{subjectData.descriptiveTags.length > 0
							? `[${subjectData.descriptiveTags
									.map((tag) => `"${tag}"`)
									.join(", ")}]`
							: "No descriptive tags available"}
					</p>
					<p>
						<strong>Context Tags: </strong> {subjectData.contextTags}
					</p>
				</div>
			) : (
				<p>No subject data found for ID: {subjectID}</p>
			)}
		</div>
	);
}
