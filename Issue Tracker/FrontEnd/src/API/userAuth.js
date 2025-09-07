const USERPREFIX = "/user";
const USERREGISTER = "/register";
const USERLOGIN = "/login";
const USER_TEST_JWT = "/protected_test";
const REFRESH_TOKEN = "/refresh";
const USERLOGOUT = "/logout";

export const userSignUp = async (dataToSend) => {
  try {
    const response = await fetch(`${USERPREFIX}${USERREGISTER}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToSend),
    });

    const data = await response.json();

    if (!data.ok) {
      console.error("Registering user error");
      return data.message;
    }

    console.log("----------------------------");
    console.log("From UserSignUp");
    console.log({ response, data });
    console.log(`Sent to the backend: ${data.status}`);
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};

export const userLogIn = async (dataToSend) => {
  try {
    const response = await fetch(`${USERPREFIX}${USERLOGIN}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToSend),
      credentials: "include",
    });

    const data = await response.json();

    if (!data.ok) {
      console.error("Loggin in Error");
      console.log(data);
      return data;
    }

    console.log("----------------------------");
    console.log("From UserSignUp");
    console.log({ response, data });
    console.log(`Sent to the backend: ${data.status}`);
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};

export const userLogout = async () => {
//   const csrfToken = getCookie("csrf_refresh_token");
  try {
    const response = await fetch(`${USERPREFIX}${USERLOGOUT}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // "X-CSRF-TOKEN": csrfToken,
      },
      credentials: "include",
    });

    const data = await response.json();

    if (!data.ok) {
      console.error("Loggin in Error");
      console.log(data);
      return data;
    }

    console.log("----------------------------");
    console.log("From UserSignUp");
    console.log({ response, data });
    console.log(`Sent to the backend: ${data.status}`);
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};

export const testing = async () => {
  try {
    const response = await fetch(`${USERPREFIX}${USER_TEST_JWT}`);

    const data = await response.json();

    if (!data.ok) {
      console.error("Access token expired");
      console.log(data);
      return data;
    }

    console.log("----------------------------");
    console.log("From Testing");
    console.log({ response, data });
    console.log(`Sent to the backend: ${data.status}`);
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}
