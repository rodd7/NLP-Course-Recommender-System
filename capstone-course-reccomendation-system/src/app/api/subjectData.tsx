"use server";
import { MongoClient, ServerApiVersion } from "mongodb";
import dotenv from "dotenv";

dotenv.config();

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

const uri = `mongodb+srv://crswebsrvhandle:${process.env.MONGODB_PASSWORD}@cluster0.d9bow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`;

// Create a new MongoClient
const client = new MongoClient(uri, {
	serverApi: {
		version: ServerApiVersion.v1,
		strict: true,
		deprecationErrors: true,
	},
});

export async function getSubjectData(subjectID: number) {
	try {
		await client.connect();

		const database = client.db("subject");
		const collection = database.collection<Subject>("subjects");

		const query = { subjectID: subjectID };
		const results = await collection.find(query).toArray();

		const plainResults = results.map((result) => ({
			...result,
			_id: result._id.toString(),
		}));

		return plainResults;
	} catch (error) {
		console.error("Error occurred while searching for subjects:", error);
	} finally {
		await client.close();
	}
}
