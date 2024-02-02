"use client";
import React, { useEffect, useState } from "react";
import { Button, Card, Container, Form } from "react-bootstrap";
import useWebSocket from "react-use-websocket";

type Result = {
  id: number;
  genome_name: string;
  start_index: number;
  end_index: number;
  match_found: boolean;
};
type Submission = {
  id: number;
  initiated_on: string;
  completed_on?: string;
  status: string;
  dna_sequence: string;
  result?: Result;
};

function SubmissionCard({
  submission,
}: {
  submission: Submission;
}): React.JSX.Element {
  const hasResult = submission.result !== null;
  const result = submission?.result;
  return (
    <Card>
      <ul>
        <li>Submitted sequence: {submission.dna_sequence}</li>
        <li>Submitted on: {submission.initiated_on}</li>
        <li>Completed on: {submission.completed_on ?? "N/A"}</li>
      </ul>
      {!result && "Alignment results pending"}
      {hasResult && result?.match_found && (
        <ul>
          <li>Genome name: {result.genome_name}</li>
          <li>
            Index range: [{result.start_index}, {result.end_index}]
          </li>
        </ul>
      )}
      {hasResult && !result?.match_found && "No match found"}
    </Card>
  );
}

export default function Page() {
  let host = "localhost";
  if (process.env.NODE_ENV === "production") {
    host = "24.199.71.90";
  }

  const [dnaSequence, setDnaSequence] = useState<string>("");
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [previousMessage, setPreviousMessage] = useState<string | null>(null);
  const { lastMessage, sendJsonMessage } = useWebSocket(`ws://${host}:8000/`);

  async function getSubmissions() {
    try {
      const response = await fetch(`http://${host}:8000/api/submissions/`);
      const data: Submission[] = await response.json();
      setSubmissions(data);
    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {
    getSubmissions();
  }, []);

  useEffect(() => {
    if (lastMessage !== null && lastMessage?.data !== previousMessage) {
      const data = JSON.parse(lastMessage.data);
      const payload = data.payload;
      setPreviousMessage(lastMessage.data);
      switch (data.action) {
        case "new_submission":
          setSubmissions([...submissions, payload]);
          break;
        case "update_submission":
          submissions.some((submission) => {
            if (submission.id === payload.id) {
              submission.status = payload.status;
              submission.completed_on = payload.completed_on;
              submission.result = payload.result;
              return true;
            }
          });
          break;
        default:
          break;
      }
    }
  }, [lastMessage]);

  return (
    <Container>
      <h1>Genome Alignment</h1>
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
            setDnaSequence("");
            sendJsonMessage({
              action: "create_submission",
              payload: {
                dna_sequence: dnaSequence.toUpperCase().replaceAll(" ", ""),
                initiated_on: new Date().toISOString(),
              },
            });
          }}
        >
          Find Genome
        </Button>
      </Form>
      <div style={{ marginTop: "1rem" }}>
        <h1>Submissions</h1>
        <div>
          {submissions &&
            submissions.map((submission) => {
              return (
                <SubmissionCard key={submission.id} submission={submission} />
              );
            })}
        </div>
      </div>
    </Container>
  );
}
