import React, { useEffect, useRef, useState } from "react";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardHeader,
  MDBCardBody,
  MDBCardFooter,
  MDBIcon,
  MDBBtn
} from "mdb-react-ui-kit";
import user from './user.png'
import chatbot from './chatbot.png'
function ChatComponent() {
  const[pdfAdded,setPdf]=useState(false)
  const [messages,setMessages]=useState([])

  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  function getCurrentTime(){
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();

    // Format the time
    const formattedTime = `${hours}:${minutes}`;

    return formattedTime;
  };

  function setBotMessage(msg){
    const formattedText = msg.split('\n').map((line, index) => (
      <React.Fragment key={index}>
        {line}
        <br />
      </React.Fragment>
    ));
    const newMessage = {
      "user": 1, 
      "msg": formattedText, 
      "time": getCurrentTime()
    };
    console.log(msg)
    setMessages(prevMessages => [...prevMessages, newMessage]);
    scrollToBottom()
  }
  const handleButtonClick = () => {
    if (inputValue.trim() === '') {
      alert('Input is empty');
    } 
    else if(!pdfAdded){
      alert("Please upload a pdf first")
    }
    else {
      const formattedText = inputValue.split('\n').map((line, index) => (
        <React.Fragment key={index}>
          {line}
          <br />
        </React.Fragment>
      ));
      const newMessage = {
        "user": 0, 
        "msg": formattedText, 
        "time": getCurrentTime()
      };
      setMessages(prevMessages => [...prevMessages, newMessage]);
      scrollToBottom()
      sendRequest(inputValue)
      setInputValue("")
    }
  };
  const url = 'http://127.0.0.1:4000/query';

  async function sendRequest(query) {
    
      const data = {
        query: inputValue
      };
  
      // Send the POST request
      await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      }).then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setBotMessage(data.result);
        console.log(data.result); 
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }


  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };
  const uploadPDF = async () => {
    const formData = new FormData();
    formData.append('pdf', selectedFile);
  
    try {
      const response = await fetch('http://127.0.0.1:4000/uploadPdf', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        console.log('PDF uploaded successfully');
        setPdf(true)
        alert("You Can Use Your ChatBoat")
        // Handle success
      } else {
        console.error('Failed to upload PDF');
        // Handle error
      }
    } catch (error) {
      console.error('Error uploading PDF:', error);
      // Handle error
    }
  };
  const scrollContainerRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, []);

  const scrollToBottom = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  };
  return (
    <MDBContainer fluid className="py-5" style={{ backgroundColor: "#eee" }}>
      <MDBRow className="d-flex justify-content-center">
        <MDBCol md="10" lg="8" xl="6">
          <MDBCard id="chat2" style={{ borderRadius: "15px" }}>
            <MDBCardHeader className="d-flex justify-content-between align-items-center p-3">
              <h5 className="mb-0">Chat</h5>
              <input className=" text-black rounded-md text-sm shadow-sm p-2" type="file" accept=".pdf " onChange={handleFileChange} />

              <MDBBtn color="primary bg-blue-700 " size="sm" rippleColor="dark" onClick={uploadPDF}>
                Add Pdf to Chat
              </MDBBtn>
              
            </MDBCardHeader>
            <div className="overflow-y-auto max-h-300"
              suppressScrollX
              style={{ position: "relative", height: "400px",scrollBehavior: 'smooth' }}
              ref={scrollContainerRef}

            >
              <MDBCardBody>
              {messages.map((message, index) => (
                <React.Fragment key={index}>
                  {message.user === 1 && (
                    <div className="d-flex flex-row justify-content-start">
                      <img
                        src={chatbot}
                        alt="avatar 1"
                        style={{ width: "45px", height: "100%" }}
                      />
                      <div>
                        <p
                          className="small p-2 ms-3 mb-1 rounded-3"
                          style={{ backgroundColor: "#f5f6f7" }}
                        >
                          {message.msg}
                        </p>
                        <p className="small ms-3 mb-3 rounded-3 text-muted">
                          {message.time}
                        </p>
                      </div>
                    </div>
                  )}
                  {message.user === 0 && (
                    <div className="d-flex flex-row justify-content-end mb-4 pt-1">
                      <div>
                        <p className="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">
                        {message.msg}
                        </p>
                        <p className="small me-3 mb-3 rounded-3 text-muted d-flex justify-content-end">
                        {message.time}
                        </p>
                      </div>
                      <img
                        src={user}
                        alt="avatar 1"
                        style={{ width: "45px", height: "100%" }}
                      />
                    </div>
                  )}
                </React.Fragment>
              ))}

                

              
              </MDBCardBody>
            </div>
            <MDBCardFooter className="text-muted d-flex justify-content-start align-items-center p-3">
              <img
                src={user}
                alt="avatar 3"
                style={{ width: "45px", height: "100%" }}
              />
              <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                className="form-control form-control-lg"
                id="exampleFormControlInput1"
                placeholder="Type message"
              />

              <a className="ms-3 p-2" href="#!" onClick={handleButtonClick}>
                <MDBIcon fas icon="paper-plane" />
              </a>
            </MDBCardFooter>
          </MDBCard>
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
}
export default ChatComponent;