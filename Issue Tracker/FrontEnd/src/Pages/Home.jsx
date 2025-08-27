import TopBar from "../Components/TopBar";
import Open from "../Components/Open";
import InProgress from "../Components/InProgress";
import Resolved from "../Components/Resolved";
import IssueForm from "../Components/IssueForm";
import { useState, useEffect, createContext } from "react";
import { getData, sendData } from "../API/issuetracker";

export const handleForm = createContext();

export function Home() {
  const [showForm, SetShowForm] = useState(false);
  const [initialData, setInitialData] = useState([]);
  const [openData, setOpenData] = useState([]);
  const [prograssData, setPrograssData] = useState([]);
  const [ResolvedData, setResolvedData] = useState([]);
  const openStatus = "open";
  const progressStatus = "progress";
  const resolvedStatus = "resolved";

  useEffect(() => {
    const loadData = async () => {
      const response = await getData();
      setInitialData(response.message);
    };

    loadData();
  }, []);

  useEffect(() => {
    HandleDisplayData();
  }, [initialData]);

  const handleFormShow = () => SetShowForm(true);
  const handleFormHide = () => SetShowForm(false);

  const HandleDisplayData = () => {
    const filteredDatta = initialData.sort(
      (a, b) => b.priority_level - a.priority_level
    );

    setOpenData(filteredDatta.filter((data) => data.status == openStatus));
    setPrograssData(
      filteredDatta.filter((data) => data.status == progressStatus)
    );
    setResolvedData(
      filteredDatta.filter((data) => data.status == resolvedStatus)
    );
  };

  const handleSubmitData = async (dataToSubmit) => {
    await sendData(dataToSubmit);
    SetShowForm(false);

    const updatedData = await getData();
    setInitialData(updatedData.message);
  };

  return (
    <>
      <TopBar></TopBar>
      <div className="flex pl-5">
        <button
          className=" my-5 px-2 py-1.5 font-bold text-[clamp(20px,3vw,35px)] rounded-lg cursor-pointer transi bg-color-secondary-accent-yellow hover:bg-[hsl(38,92%,40%)] active:bg-[hsl(38,92%,40%)]"
          onClick={handleFormShow}
        >
          + New Issue
        </button>
      </div>

      {showForm && (
        <IssueForm
          data={{}}
          submitData={handleSubmitData}
          hideForm={handleFormHide}
        />
      )}

      <div className="flex flex-col items-center md:justify-evenly md:flex-row py-10 overflow-hidden bg-color-muted-gray-yellow">
        <handleForm.Provider value={{ SetShowForm }}>
          <Open datas={openData}></Open>
          <InProgress datas={prograssData}></InProgress>
          <Resolved datas={ResolvedData}></Resolved>
        </handleForm.Provider>
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
