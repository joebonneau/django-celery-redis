"use client";
import React, { useEffect, useState } from "react";
import { Button, Card, Container, Form } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

type Result = {
  id: number;
  submission_id: number;
  protein_name: string;
  loc_in_protein_seq: number;
};
type Submission = {
  id: number;
  initiated_on: string;
  completed_on?: string;
  status: string;
  dna_sequence: string;
  result?: Result;
};

export default function Page() {
  const [dnaSequence, setDnaSequence] = useState<string>("");
  const [submissions, setSubmissions] = useState<Submission[]>([]);

  async function getSubmissions() {
    try {
      const response = await fetch("http://localhost:8000/api/submissions/");
      const data: Submission[] = await response.json();
      setSubmissions(data);
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  async function createSubmission() {
    try {
      const response = await fetch("http://localhost:8000/api/submissions/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          dna_sequence: dnaSequence,
          initiated_on: new Date().toISOString(),
        }),
      });
      setSubmissions([...submissions, await response.json()]);
    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {
    getSubmissions();
  }, []);

  return (
    <Container>
      <h1>Protein Alignment</h1>
      <Form>
        <Form.Group>
          <Form.Label>DNA Sequence</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter DNA sequence"
            onChange={(e) => setDnaSequence(e.target.value)}
            value={dnaSequence}
          />
        </Form.Group>
        <Button
          className="mt-2"
          variant="primary"
          type="submit"
          disabled={!dnaSequence}
          onClick={(e) => {
            e.preventDefault();
            console.log(dnaSequence);
            setDnaSequence("");
            createSubmission();
          }}
        >
          Find Protein
        </Button>
      </Form>
      <div style={{ marginTop: "1rem" }}>
        <h1>Submissions</h1>
        <Card>
          {submissions &&
            submissions.map((submission) => {
              console.log(submission);
              return (
                <p key={submission.id}>
                  {submission.initiated_on},{" "}
                  {submission.completed_on ?? "incomplete"}, {submission.status}
                  , {submission.dna_sequence},{" "}
                  {submission.result
                    ? submission.result.protein_name
                    : "no result"}
                </p>
              );
            })}
        </Card>
      </div>
    </Container>
  );
}
