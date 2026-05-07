import os
import json
from pathlib import Path
from dotenv import load_dotenv
from src.utils.csv_manager import load_csv
from src.mashines.fragmentanalyzer.api_manager import get_state_id, get_entities
from src.config.settings import get_fa_qc, get_workflow_id_by_name, set_workflow_id, get_local_directory, get_fragmentanalyzer_id, get_workflow_id
from src.mashines.fragmentanalyzer.data_extracter import extract_sample_peaks
from src.mashines.fragmentanalyzer.sample_classifier import sample_classifier

def main(session):
    load_dotenv()
    workflow_id = get_workflow_id_by_name(session, os.getenv("WORKFLOW"))
    set_workflow_id(workflow_id)
    
    # Get Data from DiData from Visualization Nodes
    qcs = [get_fa_qc("pcr"), get_fa_qc("lib")]
    state_ids = get_state_id(session, qcs, get_workflow_id())
    didata_sample_names = get_entities(session, state_ids.values())
    didata_sample_names = [
        sample["sample_id"]
        for state in didata_sample_names.get("states", [])
        for sample in state.get("samples", [])
    ]

    # Load Csv File
    csv_df = load_csv(Path(get_local_directory(get_fragmentanalyzer_id())))
    sample_peaks = extract_sample_peaks(csv_df)
    
    qc = sample_classifier(sample_peaks.keys(), didata_sample_names)
    
    
    # debug
    # print(json.dumps(samples, indent=4))
    # print("\n")
    # print(sample_names)
    
    

if __name__ == "__main__":
    main()
    
    
    
# PHP User Route in DiData
    
''' Powered by DiData
* You have access to $this->request the current request
* You have access to $this->response the response to return
* You have access to $this->request->route('a') to get url params for route subpath ex: /home/{a}
*
* Examples:
*
* Set response content:
* $this->response->setResponseContent('Hello, World!');
*
* Set response status code:
* $this->response->setResponseStatusCode(200);
*
* Set response headers:
* $this->response->setResponseHeaders(['Content-Type' => 'application/json']);
*
* Download a file:
* $this->response->download('/path/to/file.pdf', 'document.pdf');
*
* Stream a file download:
* $this->response->streamDownload(function() {
*     echo 'File content here';
* }, 'filename.txt');
*
* Add a custom method:
* $this->addMethod('customMethod', function() {
*     return 'Custom method result';
* });
*
* Set specific HTTP status codes:
* $this->response->ok();                  // 200 OK
* $this->response->created();             // 201 Created
* $this->response->accepted();            // 202 Accepted
* $this->response->noContent();           // 204 No Content
* $this->response->movedPermanently();    // 301 Moved Permanently
* $this->response->found();               // 302 Found
* $this->response->badRequest();          // 400 Bad Request
* $this->response->unauthorized();        // 401 Unauthorized
* $this->response->forbidden();           // 403 Forbidden
* $this->response->notFound();            // 404 Not Found
* $this->response->requestTimeout();      // 408 Request Timeout
* $this->response->conflict();            // 409 Conflict
* $this->response->unprocessableEntity(); // 422 Unprocessable Entity
* $this->response->tooManyRequests();     // 429 Too Many Requests
*
* Example response:
* $this->response->setResponseHeaders(['Content-Type' => 'application/json']);
* $this->response->setResponseContent(json_encode(['message' => 'Success']));
* $this->response->ok();
*
* Access route parameters:
* $param = $this->request->route('paramName');
'''