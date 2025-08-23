import TopBar from "./TopBar";
import Open from "./Open";
import InProgress from "./InProgress";
import Resolved from "./Resolved";
import IssueForm from "./IssueForm";
import { useState } from "react";

export default function Home() {
  const [showForm, SetShowForm] = useState(false);

  const handleFormShow = () => SetShowForm(true);
  const handleFormHide = () => SetShowForm(false);

  return (
    <>
      <TopBar title="Issue Tracker"></TopBar>
      <div className="flex pl-5">
        <button
          className=" my-5 px-2 py-1.5 font-bold text-[clamp(20px,3vw,35px)] rounded-lg cursor-pointer transi bg-color-secondary-accent-yellow hover:bg-[hsl(38,92%,40%)] active:bg-[hsl(38,92%,40%)]"
          onClick={handleFormShow}
        >
          + New Issue
        </button>
      </div>

      {showForm && <IssueForm hideForm={handleFormHide} />}

      <div className="flex flex-col items-center md:justify-evenly md:flex-row py-10 overflow-hidden bg-color-muted-gray-yellow">
        <Open></Open>
        <InProgress></InProgress>
        <Resolved></Resolved>
      </div>
    </>
  );
}

// ┌─────────────────────────────────────────────┐
// │                 🐞 Issue Tracker             │
// │─────────────────────────────────────────────│
// │ [ + New Issue ]                              │
// │                                             │
// │ ┌────── Open ──────┐  ┌── In Progress ─┐  ┌── Resolved ──┐
// │ │ #45  Login fails │  │ #39  CSS bugs  │  │ #21  Fixed   │
// │ │ High priority    │  │ Medium prio.   │  │ Login fixed  │
// │ │ [View] [Edit]    │  │ [View] [Edit]  │  │ [View]       │
// │ └──────────────────┘  └────────────────┘  └──────────────┘
// │                                             │
// └─────────────────────────────────────────────┘
