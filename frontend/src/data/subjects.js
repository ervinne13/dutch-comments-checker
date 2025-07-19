// Hardcoded data for subjects and comments
export const subjects = [
  {
    id: 1,
    title: "Subject A",
    commentCount: 5,
    flaggedCount: 2,
    comments: [
      {
        text: "This is a comment.",
        llmReasoning: "Flagged for spam.",
        spam: 0.1,
        toxic: 0.7
      },
      {
        text: "Another comment.",
        llmReasoning: "Clean.",
        spam: 0.0,
        toxic: 0.0
      }
      // ...more comments
    ]
  },
  {
    id: 2,
    title: "Subject B",
    commentCount: 3,
    flaggedCount: 1,
    comments: [
      {
        text: "Comment for B.",
        llmReasoning: "Flagged for toxicity.",
        spam: 0.0,
        toxic: 0.8
      }
      // ...more comments
    ]
  }
  // ...more subjects
];
