using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class trafficManager : MonoBehaviour
{
    List<List<Vector3>> positions; //positions per frame
    List<GameObject> cars; //agents
    private float timer= 0f; //timer control
    private float timeToUpdate = 5f; //time to request more positions
    public float dt; // How much to move a 

    IEnumerator InitializeModel()
    {
        WWWForm form = new WWWForm();
        string url= "http://127.0.0.1:5000/init";
        using (UnityWebRequest www = UnityWebRequest.Get(url)){
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");
            yield return www.SendWebRequest();
            if(www.result == UnityWebRequest.Result.ConnectionError){
                Debug.Log(www.error);
            }
            else{
                string txt = www.downloadHandler.text;
                Debug.Log(txt);
            }
        }
    }
    IEnumerator DoStepGetPosition()
    {
        WWWForm form = new WWWForm();
        string url= "http://127.0.0.1:5000/step";
        using (UnityWebRequest www = UnityWebRequest.Get(url)){
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");
            yield return www.SendWebRequest();

            if(www.result == UnityWebRequest.Result.ConnectionError){
                Debug.Log(www.error);
            }
            else{
                string txt = www.downloadHandler.text;
                Debug.Log("The result after step");
                Debug.Log(txt);
            }
        }
    }


    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(InitializeModel());
        
    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime; // Increment timer by the time since last frame

        if (timer >= timeToUpdate)
        {
            Debug.Log("passed 5 seconds");
            Debug.Log("Calling DoStepGetPosition");
            StartCoroutine(DoStepGetPosition()); // Call the coroutine
            timer = 0f; // Reset the timer
        }
        
    }
}
