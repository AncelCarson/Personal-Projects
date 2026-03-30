Imports System
Imports System.Collections.Generic
Imports System.Linq

Module Program
    Sub Main()

        ' =========================
        ' Basics: Printing & Input
        ' =========================
        Console.WriteLine("Hello, World!")

        Console.Write("Enter your name: ")
        Dim name As String = Console.ReadLine()

        ' String formatting
        Console.WriteLine("Hello, {0}", name)
        Console.WriteLine($"Hello, {name}") ' Interpolation (modern VB)

        ' =========================
        ' Variables & Data Types
        ' =========================
        Dim age As Integer = 25
        Dim height As Double = 5.9
        Dim isStudent As Boolean = True

        ' =========================
        ' Basic Arithmetic
        ' =========================
        Dim x As Integer = 10
        Dim y As Integer = 5

        Dim sumResult = x + y
        Dim difference = x - y
        Dim product = x * y
        Dim division = x / y
        Dim remainder = x Mod y

        ' =========================
        ' Lists (Collections)
        ' =========================
        Dim fruits As New List(Of String) From {"apple", "banana", "cherry"}
        Dim firstFruit As String = fruits(0)
        fruits.Add("orange")
        Dim numFruits As Integer = fruits.Count

        ' =========================
        ' Control Structures
        ' =========================
        If age >= 18 Then
            Console.WriteLine("You are an adult.")
        Else
            Console.WriteLine("You are a minor.")
        End If

        ' =========================
        ' Loops
        ' =========================
        For i As Integer = 0 To 4
            Console.WriteLine("Iteration {0}", i)
        Next

        Dim counter As Integer = 0
        While counter < 5
            Console.WriteLine("While loop iteration {0}", counter)
            counter += 1
        End While

        ' =========================
        ' Functions
        ' =========================
        Dim message As String = Greet("Alice")

        ' =========================
        ' Classes & Objects
        ' =========================
        Dim myDog As New Dog("Buddy", "Golden Retriever")
        Dim dogSound As String = myDog.Bark()

        ' =========================
        ' Built-in Functions
        ' =========================
        Dim numbers As New List(Of Integer) From {3, 1, 4, 1, 5}
        Dim minVal = numbers.Min()
        Dim maxVal = numbers.Max()
        Dim sumVal = numbers.Sum()

        ' =========================
        ' File Handling
        ' =========================
        Dim path As String = "sample.txt"
        System.IO.File.WriteAllText(path, "This is a sample file.")
        Dim fileContents As String = System.IO.File.ReadAllText(path)

        ' =========================
        ' Exception Handling
        ' =========================
        Dim result As String
        Try
            Dim bad = 10 / 0
            result = bad.ToString()
        Catch ex As DivideByZeroException
            result = "Error: Division by zero"
        End Try

        ' =========================
        ' Lambda Expressions
        ' =========================
        Dim add = Function(a As Integer, b As Integer) a + b
        Dim lambdaResult = add(3, 4)

        ' LINQ + Lambda example
        Dim evenNumbers = numbers.Where(Function(n) n Mod 2 = 0).ToList()

        ' =========================
        ' Output Section
        ' =========================
        Console.WriteLine(vbCrLf & "=== Results ===")

        Console.WriteLine("Variables: {0}, {1}, {2}", age, height, isStudent)
        Console.WriteLine("Math: {0}, {1}, {2}, {3}, {4}",
                          sumResult, difference, product, division, remainder)

        Console.WriteLine("Fruits: " & String.Join(", ", fruits))
        Console.WriteLine("Function: " & message)
        Console.WriteLine("Dog: " & dogSound)

        Console.WriteLine("Min/Max/Sum: {0}, {1}, {2}", minVal, maxVal, sumVal)

        Console.WriteLine("File contents: " & fileContents)
        Console.WriteLine("Exception result: " & result)

        Console.WriteLine("Lambda result: " & lambdaResult)
        Console.WriteLine("Even numbers: " & String.Join(", ", evenNumbers))

    End Sub

    ' =========================
    ' Function Definition
    ' =========================
    Function Greet(name As String) As String
        Return "Hello, " & name
    End Function

End Module

' =========================
' Class Definition
' =========================
Class Dog
    Public Property Name As String
    Public Property Breed As String

    Public Sub New(n As String, b As String)
        Name = n
        Breed = b
    End Sub

    Public Function Bark() As String
        Return Name & " barks!"
    End Function
End Class