using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class WebClient : MonoBehaviour
{
    [System.Serializable]
    public class Agent
    {
        public int id; // ID del agente
        public int x;  // Coordenada x
        public int y;  // Coordenada y
    }

    public List<Vector3> agentPositions; // Lista para almacenar posiciones de los agentes

    void Start()
    {
        StartCoroutine(RequestPositionStep());
    }

    public IEnumerator RequestPositionStep()
    {
        string stepUrl = "http://127.0.0.1:5000/step"; // URL del endpoint step
        using (UnityWebRequest www = UnityWebRequest.Get(stepUrl))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError(www.error);
                yield break;
            }
            else
            {
                string txt = www.downloadHandler.text;
                Debug.Log("Received Step JSON: " + txt);

                // Deserializamos el JSON en una lista de objetos Agent
                List<Agent> agents = JsonUtility.FromJson<Wrapper<Agent>>(WrapJson(txt)).data;

                if (agents == null)
                {
                    Debug.LogError("Failed to deserialize Step JSON.");
                    yield break;
                }

                SaveDataToList(agents);
                PrintDataToConsole();
            }
        }
    }

    void SaveDataToList(List<Agent> agents)
    {
        agentPositions = new List<Vector3>();

        foreach (var agent in agents)
        {
            // Agregar las posiciones de los agentes a la lista
            agentPositions.Add(new Vector3(agent.x, 5, agent.y)); // y = 5 para altura
        }
    }

    void PrintDataToConsole()
    {
        Debug.Log("Agent Positions:");
        foreach (var position in agentPositions)
        {
            Debug.Log(position);
        }
    }

    // Wrapper para manejar JSON de arrays
    private string WrapJson(string json)
    {
        return "{\"data\":" + json + "}";
    }

    // Clase contenedora para deserializar arrays
    [System.Serializable]
    public class Wrapper<T>
    {
        public List<T> data;
    }
}
