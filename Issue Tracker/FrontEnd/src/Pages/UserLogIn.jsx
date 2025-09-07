import TopBar from "../Components/TopBar";
import { useState, useEffect } from "react";
import { userSignUp, userLogIn, userLogout, testing } from "../API/userAuth";

export default function UserLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [usernameLogin, setUsernameLogin] = useState("");
  const [passwordLogin, setPasswordLogin] = useState("");

  const [userData, setUserData] = useState([]);

  useEffect(() => {
    const handleTesting = async () => {
      const userTesting = await testing();

      console.log(userTesting);
      setUserData(userTesting.user);
    };

    handleTesting();
  }, []);

  const onSubmit = async (e) => {
    e.preventDefault();

    const submitData = {};

    submitData.username = username.trim();
    submitData.password = password.trim();

    try {
      const response = await userSignUp(submitData);
      console.log(response.message);
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    const logInData = {};

    logInData.username = usernameLogin.trim();
    logInData.password = passwordLogin.trim();

    try {
      const response = await userLogIn(logInData);
      console.log(response.ok);
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <>
      <TopBar titleHome="Sign up/Log in" />
      <button
        className="flex mx-auto text-7xl cursor-pointer"
        onClick={userLogout}
      >
        {userData ? userData.username : "Logout"}
      </button>
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
            onChange={(e) => setUsername(e.target.value)}
            className="bg-white ml-5"
          />
          <br />
          <br />

          <label htmlFor="password">Enter passowrd</label>
          <input
            type="password"
            name="password"
            id="password"
            onChange={(e) => setPassword(e.target.value)}
            className="bg-white ml-5"
          />
          <button type="submit" className="flex mt-5 mx-auto">
            Submmit
          </button>
        </form>
      </div>

      <div className="flex">
        <form
          action=""
          onSubmit={handleLogin}
          className="bg-color-neutral-dark-text-yellow font-black text-green-500 text-2xl rounded-lg inline-block mx-auto mt-50 p-15"
        >
          <label htmlFor="usernameLogin">Enter username</label>
          <input
            type="text"
            name="usernameLogin"
            id="usernameLogin"
            onChange={(e) => setUsernameLogin(e.target.value)}
            className="bg-white ml-5"
          />
          <br />
          <br />

          <label htmlFor="passwordlogin">Enter password</label>
          <input
            type="password"
            name="passwordlogin"
            id="passwordlogin"
            onChange={(e) => setPasswordLogin(e.target.value)}
            className="bg-white ml-5"
          />
          <button type="submit" className="flex mt-5 mx-auto">
            Submmit
          </button>
        </form>
      </div>
    </>
  );
}
