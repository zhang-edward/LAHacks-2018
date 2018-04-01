import React, { Component } from 'react';
import CsvParser from './components/CsvParser';
import './styles/App.css';

class App extends Component {

  render() {
    return (
      <div className="app">
        <header className="title">
          <h1>Instruct.ai</h1>
        </header>

        <p>
          Welcome to Instruct.ai. To get started, upload a video file.
        </p>

        <div className="form-container">
          <div className="form">
            <form action="/" encType="multipart/form-data" method="post">
                <input type="file" name="upload"/>
                <input type="submit" value="Upload"/>
            </form>
          </div>
        </div>
        I'm a csv parser!
        <CsvParser/>
      </div>
    );
  }
}

export default App;