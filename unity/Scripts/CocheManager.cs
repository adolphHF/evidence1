using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class CocheManager : MonoBehaviour
{
    public WebClient webClient;        // Referencia al WebClient
    public GameObject cochePrefab;    // Prefab del coche
    public float speed = 5f;           // Velocidad de movimiento

    private List<GameObject> cochesInstanciados = new List<GameObject>(); // Lista de instancias de coches
    private bool[] isMoving;           // Control para movimiento de cada coche
    private Vector3[] directions;      // Direcciones actuales de los coches
    private Vector3[] positions;       // Posiciones actuales de los coches

    private bool isWaitingForServerResponse;

IEnumerator Start()
{
    if (webClient == null || cochePrefab == null)
    {
        Debug.LogError("WebClient o prefab no configurados.");
        yield break;
    }

    // Esperar la primera posición de los coches desde el servidor
    yield return StartCoroutine(webClient.RequestPositionStep());

    if (webClient.agentPositions == null || webClient.agentPositions.Count == 0)
    {
        Debug.LogError("No se recibieron posiciones de los agentes desde el servidor.");
        yield break;
    }

    int agentCount = webClient.agentPositions.Count;

    isMoving = new bool[agentCount];
    directions = new Vector3[agentCount];
    positions = new Vector3[agentCount];

    // Instanciar coches con las posiciones iniciales
    for (int i = 0; i < agentCount; i++)
    {
        Vector3 startPosition = webClient.agentPositions[i];
        GameObject coche = Instantiate(cochePrefab, startPosition, Quaternion.identity);
        cochesInstanciados.Add(coche);

        positions[i] = startPosition;
        directions[i] = Vector3.forward; // Dirección inicial
    }
}


void Update()
{
    if (isMoving == null || isMoving.Length == 0)
        return;

    if (isWaitingForServerResponse)
        return;

    if (isMoving.All(value => !value))
    {
        StartCoroutine(HandleServerRequest());
    }
    else
    {
        for (int i = 0; i < cochesInstanciados.Count; i++)
        {
            // Lógica de movimiento
            Vector3 currentPosition = positions[i];
            Vector3 targetPosition = webClient.agentPositions[i];
            Vector3 directionToTarget = VecOps.Normalize(targetPosition - currentPosition);
            float angle = VecOps.Angle(directions[i], directionToTarget);

            if (Vector3.Distance(currentPosition, targetPosition) > 0.1f || angle > 0.1f)
            {
                if (angle > 0.1f)
                {
                    // Manejar rotación
                    float rotationDirection = Mathf.Sign(VecOps.CrossProduct(directions[i], directionToTarget).y);
                    float rotationStep = Mathf.Min(angle, speed * Time.deltaTime * 50);
                    Matrix4x4 rotationMatrix = VecOps.RotateYM(rotationStep * rotationDirection);
                    directions[i] = VecOps.Normalize(rotationMatrix.MultiplyPoint3x4(directions[i]));
                }
                else
                {
                    // Manejar traslación
                    Matrix4x4 translationMatrix = VecOps.TranslateM(directions[i] * (speed * Time.deltaTime));
                    currentPosition = VecOps.MultiplyPoint(currentPosition, translationMatrix);
                    positions[i] = currentPosition;
                }

                // Actualizar posición y rotación del coche
                ApplyMatrixToCoche(cochesInstanciados[i], positions[i], directions[i]);
            }
            else
            {
                isMoving[i] = false; // Detener movimiento si está cerca del objetivo
            }
        }
    }
}


    private void ApplyMatrixToCoche(GameObject coche, Vector3 position, Vector3 direction)
    {
        // Calcular la matriz de transformación
        Matrix4x4 transformMatrix = VecOps.TranslateM(position) * VecOps.RotateYM(VecOps.Angle(Vector3.forward, direction));

        // Aplicar posición y rotación usando la matriz
        coche.transform.position = VecOps.MultiplyPoint(Vector3.zero, transformMatrix); // Nueva posición
        coche.transform.rotation = Quaternion.LookRotation(direction);                 // Nueva rotación
    }

    IEnumerator HandleServerRequest()
    {
        isWaitingForServerResponse = true;

        // Esperar la respuesta del servidor
        yield return StartCoroutine(webClient.RequestPositionStep());

        // Configurar todos los coches para moverse
        for (int i = 0; i < cochesInstanciados.Count; i++)
        {
            isMoving[i] = true;
        }

        isWaitingForServerResponse = false;
    }
}
