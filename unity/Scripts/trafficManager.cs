using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class TrafficManager : MonoBehaviour
{
    public List<GameObject> carPrefabs;
    private List<Vector3> carPositions = new List<Vector3>(); 
    private List<Vector3> targetPositions = new List<Vector3>(); 
    private List<Vector3> currentDirections = new List<Vector3>(); 
    private List<bool> isRotating = new List<bool>(); 
    public float fixedY = .4f; 
    public float moveSpeed = 5f; 
    public float rotationSpeed = 90f; 
    private float timer = 0f; 
    private float timeToUpdate = 1f; 

    private List<GameObject> cars = new List<GameObject>(); 

    IEnumerator InitializeModel()
    {
        string url = "http://127.0.0.1:5000/init";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError($"Error fetching init data: {www.error}");
            }
            else
            {
                string jsonResponse = www.downloadHandler.text;
                Debug.Log($"Received init data: {jsonResponse}");

                List<Vector3> initialPositions = ParsePositions(jsonResponse);

                for (int i = 0; i < initialPositions.Count; i++)
                {
                    Vector3 position = initialPositions[i];
                    GameObject prefab = carPrefabs[i % carPrefabs.Count]; 
                    GameObject car = Instantiate(prefab);

                    Rigidbody rb = car.GetComponent<Rigidbody>();
                    if (rb == null)
                    {
                        rb = car.AddComponent<Rigidbody>();
                        rb.isKinematic = true; 
                        rb.useGravity = false; 
                    }

                    cars.Add(car);
                    carPositions.Add(position); 
                    targetPositions.Add(position); 
                    currentDirections.Add(Vector3.forward); 
                    isRotating.Add(false); 
                }
            }
        }
    }

    IEnumerator DoStepGetPosition()
    {
        string url = "http://127.0.0.1:5000/step";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError($"Error fetching step data: {www.error}");
            }
            else
            {
                string jsonResponse = www.downloadHandler.text;
                Debug.Log($"Received step data: {jsonResponse}");

                List<Vector3> newPositions = ParsePositions(jsonResponse);

                for (int i = 0; i < cars.Count && i < newPositions.Count; i++)
                {
                    targetPositions[i] = newPositions[i]; 
                    isRotating[i] = true; 
                }
            }
        }
    }
    
    private Vector3 GetIntermediateTarget(Vector3 currentPos, Vector3 targetPos)
{
    if (Mathf.Abs(targetPos.x - currentPos.x) > 0.1f)
    {
        return new Vector3(targetPos.x, fixedY, currentPos.z); 
    }
    else
    {
        return targetPos; 
    }
}



    void Start()
    {
        StartCoroutine(InitializeModel());
    }
    private bool RequestNextTarget(int carIndex)
    {
        if (carIndex < targetPositions.Count - 1)
        {
            targetPositions[carIndex] = targetPositions[carIndex + 1];
            return true;
        }
        else
        {
            return false;
        }
    }

void Update()
{
    for (int i = 0; i < cars.Count; i++)
    {
        Vector3 currentPos = carPositions[i];
        Vector3 targetPos = targetPositions[i];
        Vector3 directionToTarget = targetPos - currentPos;

        if (directionToTarget.sqrMagnitude > 0.0001f)
        {
            directionToTarget = VecOps.Normalize(directionToTarget);
        }
        else
        {
            //Debug.LogWarning($"Car {i} has reached its target. Skipping rotation and movement.");
            continue; 
        }

        if (IsCollisionDetected(i, targetPos))
        {
            Debug.Log($"Car {i} is waiting to avoid collision.");
            continue; // Saltar movimiento si se detecta colisión
        }

        if (isRotating[i])
        {
            // Rotar hacia el objetivo
            float angle = VecOps.Angle(currentDirections[i], directionToTarget);
            float rotationStep = rotationSpeed * Time.deltaTime;

            if (angle > 0.1f)
            {
                float rotationDirection = Mathf.Sign(VecOps.CrossProduct(currentDirections[i], directionToTarget).y);
                float stepAngle = Mathf.Min(angle, rotationStep);

                Matrix4x4 rotationMatrix = VecOps.RotateYM(stepAngle * rotationDirection);
                currentDirections[i] = VecOps.Normalize(rotationMatrix.MultiplyPoint3x4(currentDirections[i]));
            }
            else
            {
                currentDirections[i] = directionToTarget; // Asegurar dirección exacta
                isRotating[i] = false; // Rotación completada
            }
        }
        else
        {
            // Mover hacia el objetivo
            if (VecOps.Magnitude(targetPos - currentPos) > moveSpeed * Time.deltaTime)
            {
                Vector3 step = currentDirections[i] * moveSpeed * Time.deltaTime;
                carPositions[i] += step;
            }
            else
            {
                carPositions[i] = targetPos; // Asegurar posición exacta
                isRotating[i] = true; // Preparar rotación para el siguiente objetivo
            }
        }

        // Aplicar posición y rotación al prefab
        ApplyMatrixToPrefab(cars[i], carPositions[i], currentDirections[i]);
    }

    timer += Time.deltaTime;
    if (timer >= timeToUpdate)
    {
        StartCoroutine(DoStepGetPosition());
        timer = 0f;
    }
}

// Método para detectar colisiones
private bool IsCollisionDetected(int carIndex, Vector3 targetPosition)
{
    float collisionRadius = 1f; // Radio de seguridad

    for (int i = 0; i < carPositions.Count; i++)
    {
        if (i != carIndex) // No verificar contra sí mismo
        {
            if (VecOps.Magnitude(carPositions[i] - targetPosition) < collisionRadius)
            {
                return true; // Colisión detectada
            }
        }
    }

    return false; // No hay colisión
}





    private void ApplyMatrixToPrefab(GameObject car, Vector3 position, Vector3 direction)
    {
        Matrix4x4 constantRotationMatrix = VecOps.RotateYM(90f);
        Vector3 correctedDirection = constantRotationMatrix.MultiplyPoint3x4(direction);

        Rigidbody rb = car.GetComponent<Rigidbody>();
        if (rb != null)
        {
            rb.MovePosition(position);

            if (correctedDirection.sqrMagnitude > 0.0001f)
            {
                rb.MoveRotation(Quaternion.LookRotation(correctedDirection));
            }
        }
    }



    List<Vector3> ParsePositions(string json)
    {
        List<Vector3> positions = new List<Vector3>();

        try
        {
            List<PositionData> parsedData = JsonUtility.FromJson<Wrapper>($"{{\"positions\":{json}}}").positions;

            foreach (var entry in parsedData)
            {
                positions.Add(new Vector3(entry.x, .4f, entry.y));
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"Error parsing JSON: {ex.Message}");
        }

        return positions;
    }

    [System.Serializable]
    private class Wrapper
    {
        public List<PositionData> positions;
    }

    [System.Serializable]
    private class PositionData
    {
        public int id;
        public float x;
        public float y;
    }
}

