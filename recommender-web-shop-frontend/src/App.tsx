import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginPage from "./components/LoginPage";
import Recommendations from "./components/Recommendations";
import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/" element={<LoginPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

// function App() {
//   const handleSelectItem = (item: string) => [console.log(item)];
//   let items = ["Deadpool", "Snow white", "IronMan"];

//   return (
//     <div>
//       <ListGroup
//         items={items}
//         heading="Movies"
//         onSelectItem={handleSelectItem}
//       />{" "}
//       <Alert>
//         Hello world
//       </Alert>
//     </div>
//   );
// }
