import logo from './logo.svg';
import './App.css';
import HeaderPage from './components/header';
import { Route, Routes } from 'react-router-dom';
import FooterPage from './components/footer';
import Dashboard from './screen/dashboard';
import Login from './components/core/login';

function App() {
  return (
    <div className="App">
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
      <HeaderPage/>
      <Dashboard/>
      <FooterPage/>
      <Login/>
    </div>
  );
}

export default App;
