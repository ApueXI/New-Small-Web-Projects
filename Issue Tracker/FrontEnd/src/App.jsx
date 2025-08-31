import { Home } from "./Pages/Home";
import ViewIsssue from "./Pages/ViewIssue";
import { Routes, Route } from "react-router-dom";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/view/:id" element={<ViewIsssue />} />
    </Routes>
  );
}
