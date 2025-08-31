import TopBar from "../Components/TopBar";
import Open from "../Components/Open";
import InProgress from "../Components/InProgress";
import Resolved from "../Components/Resolved";
import IssueForm from "../Components/IssueForm";
import { useState, useEffect, createContext } from "react";
import { getData, sendData } from "../API/issuetracker";

export const LoadDataContext = createContext();

export function Home() {
  const [showForm, SetShowForm] = useState(false);
  const [openData, setOpenData] = useState([]);
  const [prograssData, setPrograssData] = useState([]);
  const [ResolvedData, setResolvedData] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const responseOpen = await getData("open");
    const responseProgress = await getData("progress");
    const responseResolved = await getData("resolved");

    setOpenData(responseOpen.message);
    setPrograssData(responseProgress.message);
    setResolvedData(responseResolved.message);
  };

  const handleFormShow = () => SetShowForm(true);
  const handleFormHide = () => SetShowForm(false);

  const handleSubmitData = async (dataToSubmit) => {
    await sendData(dataToSubmit);
    SetShowForm(false);

    loadData();
  };

  return (
    <>
      <TopBar></TopBar>
      {showForm && (
        <IssueForm
          data={{}}
          submitData={handleSubmitData}
          hideForm={handleFormHide}
        />
      )}
      <div className="flex pl-5">
        <button
          className=" my-5 px-2 py-1.5 font-bold text-[clamp(20px,3vw,35px)] rounded-lg cursor-pointer transi bg-color-secondary-accent-yellow hover:bg-[hsl(38,92%,40%)] active:bg-[hsl(38,92%,40%)]"
          onClick={handleFormShow}
        >
          + New Issue
        </button>
      </div>

      <div className="flex flex-col items-center md:justify-evenly md:flex-row py-10 overflow-hidden bg-color-muted-gray-yellow">
        <LoadDataContext.Provider value={loadData}>
          <Open datas={openData}></Open>
          <InProgress datas={prograssData}></InProgress>
          <Resolved datas={ResolvedData}></Resolved>
        </LoadDataContext.Provider>
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
