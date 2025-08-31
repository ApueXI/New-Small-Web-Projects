import TopBar from "../Components/TopBar";
import IssueForm from "../Components/IssueForm";
import { useLocation, Link, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { getIndividualData } from "../API/issuetracker";

export default function ViewIsssue() {
  const location = useLocation();
  const { id } = useParams();

  const [issueData, setIssueData] = useState(location.state?.data || null);
  const [showForm, SetShowForm] = useState(false);

  useEffect(() => {
    loadData();
  }, [id, issueData]);

  const loadData = async () => {
    if (!issueData) {
      const loadedData = await getIndividualData(id);
      console.log(loadedData);

      setIssueData(loadedData.message);
    }
  };

  const handleFormShow = () => SetShowForm(true);
  const handleFormHide = () => SetShowForm(false);

  if (!issueData) {
    return (
      <>
        <TopBar titleHome={true} titleNumber={true}></TopBar>
        <div className="flex justify-center items-center mt-20">
          <h1 className="bg-color-muted-gray-yellow text-[clamp(25px,3vw,50px)] font-black py-2 px-5 rounded-lg">
            Loading...
          </h1>
        </div>
      </>
    );
  }

  const statusCapitalize = `${issueData.status
    .charAt(0)
    .toUpperCase()}${issueData.status.slice(1)}`;

  return (
    <>
      <TopBar data={issueData} titleNumber={true}></TopBar>
      {showForm && (
        <IssueForm hideForm={handleFormHide} data={issueData}></IssueForm>
      )}
      <div className="bg-color-muted-gray-yellow w-[clamp(350px,70vw,700px)] mx-auto mt-20 rounded-lg flex-Col-Center justify-center">
        <Link
          to="/"
          className="hover:scale-125 active:scale-125 font-bold transi inline-block ml-auto mt-[-10px] mr-[-10px] py-1 px-2 rounded-lg bg-color-primary-accent-yellow text-[clamp(20px,3vw,30px)]"
        >
          Back
        </Link>
        <div className="bg-color-secondary-accent-yellow font-bold rounded-lg space-y-5 my-7 px-6 py-5 w-[85%] text-[clamp(20px,3vw,35px)]">
          <h1>
            Status: <span className="viewSpan">{statusCapitalize}</span>
          </h1>

          <h1>
            Priority Level:&nbsp;
            <span className="viewSpan">{issueData.priority_level}</span>
          </h1>

          <div>
            <h1>Details:</h1>
            <h1 className="text-justify font-medium viewSpan px-4">
              {issueData.details}
            </h1>
          </div>

          <button
            onClick={handleFormShow}
            className="mx-auto flex cursor-pointer hover:scale-125 active:scale-125 font-bold transi"
          >
            Edit
          </button>
        </div>
      </div>
    </>
  );
}
