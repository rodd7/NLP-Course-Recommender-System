"use server";
import { MongoClient, ServerApiVersion } from "mongodb";
import dotenv from "dotenv";

dotenv.config();

// Define an interface for the subjectRecommendedYear document
interface SubjectRecommendedYear {
	_id: string;
	subjectID: number;
	subjectRecommendedYear: number;
}

const uri = `mongodb+srv://crswebsrvhandle:${process.env.MONGODB_PASSWORD}@cluster0.d9bow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`;

const client = new MongoClient(uri, {
	serverApi: {
		version: ServerApiVersion.v1,
		strict: true,
		deprecationErrors: true,
	},
});

export async function findSubjectRecommendedYear(
	subjectID: number,
): Promise<SubjectRecommendedYear[]> {
	try {
		await client.connect();

		const database = client.db("subject");
		const collection = database.collection<SubjectRecommendedYear>(
			"subjectRecommendedYear",
		);

		const query = { subjectID: subjectID };
		const results = await collection.find(query).toArray();

		// Map the results and convert _id to string
		const plainResults = results.map((result) => ({
			...result,
			_id: result._id.toString(),
		}));

		return plainResults;
	} catch (error) {
		console.error("Error occurred while searching for subjects:", error);
		throw error;
	} finally {
		await client.close();
	}
}

export async function getSubjectRecommendedYear(
	subjectID: number,
): Promise<number | null> {
	try {
		await client.connect();

		const database = client.db("subject");
		const collection = database.collection<SubjectRecommendedYear>(
			"subjectRecommendedYear",
		);

		// Aggregation pipeline to get the highest subjectRecommendedYear
		const result = await collection
			.aggregate([
				{ $match: { subjectID: subjectID } }, // Match documents with the given subjectID
				{
					$group: {
						_id: "$subjectID",
						highestYear: { $max: "$subjectRecommendedYear" },
					},
				}, // Group by subjectID and get the max subjectRecommendedYear
			])
			.toArray();

		if (result.length > 0) {
			return result[0].highestYear;
		} else {
			return null; // Return null if no records found for the given subjectID
		}
	} catch (error) {
		console.error(
			"Error occurred while fetching highest subjectRecommendedYear:",
			error,
		);
		throw error;
	} finally {
		await client.close();
	}
}
