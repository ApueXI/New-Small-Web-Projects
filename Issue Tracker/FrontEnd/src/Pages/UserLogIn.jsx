import TopBar from "../Components/TopBar";
import { useState } from "react";

export default function UserLogin() {
  const [num, setNum] = useState(0);

  const onSubmit = (e) => {
    e.preventDefault();
    setNum((prevNum) => prevNum + 1);
  };
  return (
    <>
      <TopBar titleHome="Sign up/Log in" />
      <div className="flex">
        <form
          action=""
          onSubmit={onSubmit}
          className="bg-color-neutral-dark-text-yellow font-black text-green-500 text-2xl rounded-lg inline-block mx-auto mt-50 p-15"
        >
          <label htmlFor="username">Enter username</label>
          <input
            type="text"
            name="username"
            id="username"
            className="bg-white ml-5"
          />
          <br />
          <br />

          <label htmlFor="password">Enter passowrd</label>
          <input
            type="password"
            name="password"
            id="password"
            className="bg-white ml-5"
          />
          <button type="submit" className="flex mt-5 mx-auto">
            Submmit {num}
          </button>
        </form>
      </div>
    </>
  );
}
